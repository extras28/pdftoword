# PyMuPDF Deployment Issues - Solutions

## Problem

PyMuPDF compilation fails on Render due to missing C++ build tools and dependencies.

## Solutions (Try in Order)

### Solution 1: Use Alternative Requirements (Recommended)

Use the `requirements-no-pymupdf.txt` file which excludes PyMuPDF:

```yaml
# In render.yaml
buildCommand: pip install --upgrade pip && pip install -r requirements-no-pymupdf.txt
```

**Pros:**

-   ✅ No compilation issues
-   ✅ Fast deployment
-   ✅ Still works for most PDF files

**Cons:**

-   ❌ Less detailed PDF validation
-   ❌ No page count information

### Solution 2: Try Older PyMuPDF Version

Current requirements.txt uses PyMuPDF 1.23.0 (more stable):

```yaml
buildCommand: pip install --upgrade pip && pip install -r requirements.txt
```

### Solution 3: Alternative PDF Libraries

If issues persist, consider these alternatives:

```txt
# Alternative 1: Use only pdf2docx
pdf2docx==0.5.8

# Alternative 2: Use pdfplumber for validation
pdf2docx==0.5.8
pdfplumber==0.7.6

# Alternative 3: Use pypdf for validation
pdf2docx==0.5.8
pypdf==3.0.1
```

## Current Configuration

-   **Default render.yaml**: Uses requirements-no-pymupdf.txt (no PyMuPDF)
-   **Alternative render-with-pymupdf.yaml**: Uses requirements.txt (with PyMuPDF 1.23.0)

## Testing Locally

```bash
# Test without PyMuPDF
pip install -r requirements-no-pymupdf.txt
python app.py

# Test with PyMuPDF
pip install -r requirements.txt
python app.py
```

Both configurations will work - the app automatically detects PyMuPDF availability.
