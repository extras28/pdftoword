import os
import uuid
from flask import Flask, request, render_template, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import pdf2docx
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("PyMuPDF not available - using basic PDF validation")
from pathlib import Path
import time
import threading
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Create directories
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Store conversion status
conversion_status = {}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_old_files():
    """Remove files older than 5 minutes for development, immediate cleanup for production"""
    current_time = time.time()
    # Use 5 minutes for development, immediate for production
    cleanup_time = 300 if os.environ.get('FLASK_ENV') != 'production' else 60  # 5 minutes dev, 1 minute prod
    
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        for file_path in Path(folder).glob('*'):
            if current_time - file_path.stat().st_mtime > cleanup_time:
                try:
                    file_path.unlink()
                    print(f"Cleaned up old file: {file_path}")
                except:
                    pass

def cleanup_job_files(job_id):
    """Immediately clean up files for a specific job"""
    try:
        # Clean up upload file
        upload_files = list(Path(UPLOAD_FOLDER).glob(f"{job_id}.*"))
        for file_path in upload_files:
            file_path.unlink()
            print(f"Cleaned up upload file: {file_path}")
        
        # Clean up output file
        output_files = list(Path(OUTPUT_FOLDER).glob(f"{job_id}.*"))
        for file_path in output_files:
            file_path.unlink()
            print(f"Cleaned up output file: {file_path}")
        
        # Remove job status
        if job_id in conversion_status:
            del conversion_status[job_id]
            print(f"Cleaned up job status: {job_id}")
            
    except Exception as e:
        print(f"Error cleaning up job {job_id}: {e}")

def convert_pdf_to_docx(pdf_path, output_path, job_id, output_filename):
    """Convert PDF to DOCX with error handling and detailed progress"""
    try:
        conversion_status[job_id] = {
            'status': 'processing', 
            'progress': 0,
            'message': 'Initializing conversion...',
            'output_filename': output_filename
        }
        
        # Check if PDF is valid and get page count
        try:
            conversion_status[job_id].update({
                'progress': 10,
                'message': 'Validating PDF file...'
            })
            
            if PYMUPDF_AVAILABLE:
                # Use PyMuPDF for detailed validation if available
                doc = fitz.open(pdf_path)
                page_count = len(doc)
                doc.close()
                
                conversion_status[job_id].update({
                    'progress': 20,
                    'message': f'PDF validated successfully. Found {page_count} pages.'
                })
            else:
                # Basic file validation without PyMuPDF
                with open(pdf_path, 'rb') as f:
                    header = f.read(8)
                    if not header.startswith(b'%PDF-'):
                        raise Exception("Not a valid PDF file")
                
                conversion_status[job_id].update({
                    'progress': 20,
                    'message': 'PDF validated successfully.'
                })
            
        except Exception as e:
            conversion_status[job_id] = {
                'status': 'error', 
                'error': 'Invalid PDF file or file is corrupted'
            }
            return
        
        # Initialize converter
        conversion_status[job_id].update({
            'progress': 30,
            'message': 'Initializing PDF converter...'
        })
        
        cv = pdf2docx.Converter(pdf_path)
        
        conversion_status[job_id].update({
            'progress': 40,
            'message': 'Analyzing PDF structure and extracting content...'
        })
        
        # Convert PDF to DOCX
        conversion_status[job_id].update({
            'progress': 60,
            'message': 'Converting PDF to Word format...'
        })
        
        cv.convert(output_path, start=0, end=None)
        
        conversion_status[job_id].update({
            'progress': 85,
            'message': 'Finalizing Word document...'
        })
        
        cv.close()
        
        # Final completion
        conversion_status[job_id] = {
            'status': 'completed', 
            'progress': 100,
            'message': 'Conversion completed successfully!',
            'output_filename': output_filename
        }
        
    except Exception as e:
        conversion_status[job_id] = {
            'status': 'error', 
            'error': f'Conversion failed: {str(e)}'
        }

@app.route('/')
def index():
    cleanup_old_files()
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{job_id}.{file_extension}"
        pdf_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(pdf_path)
        
        # Prepare output path with original filename (without extension) + pdf_ prefix
        original_name = filename.rsplit('.', 1)[0]  # Remove .pdf extension
        output_filename = f"pdf_{original_name}.docx"
        output_path = os.path.join(OUTPUT_FOLDER, f"{job_id}.docx")  # Internal storage
        
        # Start conversion in background
        conversion_thread = threading.Thread(
            target=convert_pdf_to_docx,
            args=(pdf_path, output_path, job_id, output_filename)
        )
        conversion_thread.start()
        
        return jsonify({
            'job_id': job_id,
            'original_filename': filename,
            'output_filename': output_filename,
            'message': 'File uploaded successfully. Conversion started.'
        })
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/status/<job_id>')
def check_status(job_id):
    if job_id not in conversion_status:
        return jsonify({'error': 'Job not found'}), 404
    
    status = conversion_status[job_id]
    
    if status['status'] == 'completed':
        # Add download URL
        status['download_url'] = url_for('download_file', job_id=job_id)
    
    return jsonify(status)

@app.route('/download/<job_id>')
def download_file(job_id):
    if job_id not in conversion_status:
        return jsonify({'error': 'Job not found'}), 404
    
    if conversion_status[job_id]['status'] != 'completed':
        return jsonify({'error': 'File not ready for download'}), 400
    
    output_path = os.path.join(OUTPUT_FOLDER, f"{job_id}.docx")
    
    if not os.path.exists(output_path):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Get the original filename with pdf_ prefix
        output_filename = conversion_status[job_id].get('output_filename', 'pdf_converted_document.docx')
        
        # Create a response with the file
        response = send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
        # Schedule immediate cleanup after download
        def cleanup_after_download():
            time.sleep(2)  # Wait 2 seconds to ensure download started
            cleanup_job_files(job_id)
        
        cleanup_thread = threading.Thread(target=cleanup_after_download)
        cleanup_thread.start()
        
        return response
        
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': time.time()})

@app.route('/cleanup', methods=['POST'])
def manual_cleanup():
    """Manual cleanup endpoint for immediate file removal"""
    try:
        # Clean up all old files
        cleanup_old_files()
        
        # Count remaining files
        upload_count = len(list(Path(UPLOAD_FOLDER).glob('*')))
        output_count = len(list(Path(OUTPUT_FOLDER).glob('*')))
        
        return jsonify({
            'status': 'success',
            'message': 'Cleanup completed',
            'remaining_files': {
                'uploads': upload_count,
                'outputs': output_count
            }
        })
    except Exception as e:
        return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)
