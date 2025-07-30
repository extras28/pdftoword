import os
import uuid
from flask import Flask, request, render_template, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import pdf2docx
import fitz  # PyMuPDF
from pathlib import Path
import time
import threading
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
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
    """Remove files older than 1 hour"""
    current_time = time.time()
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        for file_path in Path(folder).glob('*'):
            if current_time - file_path.stat().st_mtime > 3600:  # 1 hour
                try:
                    file_path.unlink()
                except:
                    pass

def convert_pdf_to_docx(pdf_path, output_path, job_id):
    """Convert PDF to DOCX with error handling"""
    try:
        conversion_status[job_id] = {'status': 'processing', 'progress': 0}
        
        # Check if PDF is valid
        try:
            doc = fitz.open(pdf_path)
            page_count = len(doc)
            doc.close()
        except Exception as e:
            conversion_status[job_id] = {'status': 'error', 'error': 'Invalid PDF file'}
            return
        
        conversion_status[job_id] = {'status': 'processing', 'progress': 25}
        
        # Convert PDF to DOCX
        cv = pdf2docx.Converter(pdf_path)
        conversion_status[job_id] = {'status': 'processing', 'progress': 50}
        
        cv.convert(output_path, start=0, end=None)
        conversion_status[job_id] = {'status': 'processing', 'progress': 75}
        
        cv.close()
        conversion_status[job_id] = {'status': 'completed', 'progress': 100}
        
    except Exception as e:
        conversion_status[job_id] = {'status': 'error', 'error': str(e)}

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
        
        # Prepare output path
        output_filename = f"{job_id}.docx"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # Start conversion in background
        conversion_thread = threading.Thread(
            target=convert_pdf_to_docx,
            args=(pdf_path, output_path, job_id)
        )
        conversion_thread.start()
        
        return jsonify({
            'job_id': job_id,
            'original_filename': filename,
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
        return send_file(
            output_path,
            as_attachment=True,
            download_name='converted_document.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': time.time()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
