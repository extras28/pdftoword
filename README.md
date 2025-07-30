# PDF to Word Converter

A simple and elegant web application that converts PDF files to Word (.docx) documents using Python Flask.

## Features

-   🎯 **Drag & Drop Interface**: Easy file upload with drag and drop support
-   🔄 **Real-time Progress**: Live conversion progress with status updates
-   📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
-   🛡️ **Secure Processing**: Files are automatically cleaned up after conversion
-   ⚡ **Fast Conversion**: Efficient PDF to Word conversion preserving formatting
-   📄 **Multi-page Support**: Handles multi-page PDF documents
-   ❌ **Error Handling**: Graceful error handling for invalid files

## Tech Stack

-   **Backend**: Python Flask
-   **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
-   **PDF Processing**: pdf2docx, PyMuPDF
-   **UI Icons**: Font Awesome

## Quick Start

### Prerequisites

-   Python 3.7 or higher
-   pip (Python package installer)

### Installation

1. **Clone or download the project**

    ```bash
    git clone <repository-url>
    cd pdftoword
    ```

2. **Create a virtual environment (recommended)**

    ```bash
    python -m venv venv

    # On Windows
    venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the application**

    ```bash
    python app.py
    ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

1. **Upload a PDF**: Drag and drop a PDF file onto the upload area or click to browse
2. **Convert**: Click the "Convert to Word" button
3. **Download**: Once conversion is complete, download your Word document

## File Structure

```
pdftoword/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── Dockerfile         # Docker configuration
├── templates/
│   └── index.html     # Main HTML template
├── uploads/           # Temporary upload directory (auto-created)
└── outputs/           # Temporary output directory (auto-created)
```

## Configuration

### Environment Variables

You can customize the application using environment variables:

-   `FLASK_ENV`: Set to `development` for debug mode
-   `SECRET_KEY`: Set a secure secret key for production
-   `MAX_CONTENT_LENGTH`: Maximum file size (default: 50MB)

### File Size Limits

The application currently supports PDF files up to 50MB. To change this limit, modify the `MAX_CONTENT_LENGTH` in `app.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

## Deployment

### Option 1: Railway

1. Create a `railway.toml` file:

    ```toml
    [build]
    builder = "nixpacks"

    [deploy]
    startCommand = "python app.py"
    ```

2. Deploy:
    ```bash
    railway login
    railway init
    railway up
    ```

### Option 2: Render

1. Connect your GitHub repository to Render
2. Use these settings:
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `python app.py`

### Option 3: Docker

1. **Build the image**:

    ```bash
    docker build -t pdf-to-word-converter .
    ```

2. **Run the container**:
    ```bash
    docker run -p 5000:5000 pdf-to-word-converter
    ```

### Option 4: VPS/Cloud Server

1. **Set up your server** with Python 3.7+
2. **Clone the repository**
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Use a production WSGI server** like Gunicorn:
    ```bash
    pip install gunicorn
    gunicorn -w 4 -b 0.0.0.0:5000 app:app
    ```
5. **Set up a reverse proxy** with Nginx (optional but recommended)

## API Endpoints

-   `GET /` - Main application page
-   `POST /upload` - Upload and start conversion
-   `GET /status/<job_id>` - Check conversion status
-   `GET /download/<job_id>` - Download converted file
-   `GET /health` - Health check endpoint

## Error Handling

The application handles various error scenarios:

-   Invalid file types (only PDF accepted)
-   File size exceeding limits
-   Corrupted PDF files
-   Server errors during conversion
-   Network issues

## Security Features

-   File type validation
-   Secure filename handling
-   Automatic file cleanup (files deleted after 1 hour)
-   File size limits
-   Error message sanitization

## Browser Support

-   Chrome (recommended)
-   Firefox
-   Safari
-   Edge
-   Mobile browsers

## Troubleshooting

### Common Issues

1. **"No module named 'pdf2docx'"**

    - Solution: Make sure you've installed all requirements: `pip install -r requirements.txt`

2. **"Permission denied" errors**

    - Solution: Check file permissions for upload/output directories

3. **Large files not uploading**

    - Solution: Increase `MAX_CONTENT_LENGTH` in app.py

4. **Conversion takes too long**
    - Solution: This is normal for large PDFs. The progress bar will show the status.

### Development Mode

To run in development mode with auto-reload:

```bash
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python app.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Create an issue on GitHub
3. Check the Flask and pdf2docx documentation

## Acknowledgments

-   [pdf2docx](https://github.com/dothinking/pdf2docx) - PDF to DOCX conversion
-   [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - PDF processing
-   [Flask](https://flask.palletsprojects.com/) - Web framework
-   [Bootstrap](https://getbootstrap.com/) - UI framework
