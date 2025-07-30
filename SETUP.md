# Quick Setup Guide for PDF to Word Converter

## Prerequisites Installation

### 1. Install Python (Required)

**Option A: Official Python Installer (Recommended)**

1. Go to https://python.org/downloads/
2. Download Python 3.9 or later for Windows
3. Run the installer and **IMPORTANT**: Check "Add Python to PATH"
4. Verify installation: Open Command Prompt and run `python --version`

**Option B: Microsoft Store**

1. Open Microsoft Store
2. Search for "Python 3.9" or "Python 3.10"
3. Install the official Python package

### 2. Quick Start Commands

Once Python is installed, run these commands in PowerShell or Command Prompt:

```powershell
# Navigate to project directory
cd "c:\Users\dung.na1\CTel\dungna\pdftoword"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows PowerShell:
venv\Scripts\Activate.ps1
# On Windows Command Prompt:
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### 3. Open in Browser

Navigate to: http://localhost:5000

## Alternative: Use Docker (No Python Installation Required)

If you prefer not to install Python directly:

```powershell
# Build Docker image
docker build -t pdf-converter .

# Run container
docker run -p 5000:5000 pdf-converter
```

## Troubleshooting

### If you get "python is not recognized":

1. Restart your terminal/PowerShell
2. Make sure Python was added to PATH during installation
3. Try using `py` instead of `python`

### If you get permission errors with PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### If installation fails:

1. Update pip: `python -m pip install --upgrade pip`
2. Try installing with: `pip install --no-cache-dir -r requirements.txt`

## Features Overview

✅ **Drag & Drop PDF Upload**
✅ **Real-time Conversion Progress**
✅ **Mobile-Responsive Design**
✅ **Automatic File Cleanup**
✅ **Error Handling**
✅ **Multi-page PDF Support**
✅ **Download Converted Word Files**

## Deployment Ready

The application includes configuration files for:

-   Railway (`railway.toml`)
-   Docker (`Dockerfile`)
-   Any VPS/Cloud server

Choose your preferred deployment method from the README.md file!
