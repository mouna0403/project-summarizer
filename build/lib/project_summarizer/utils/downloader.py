"""
downloader.py
Utility for extracting text content from uploaded PDFs.
"""

import io
from pypdf import PdfReader


def extract_text_from_pdf(file) -> str:
    """Extract all text from a PDF file object (BytesIO or UploadedFile)."""
    reader = PdfReader(io.BytesIO(file.read()))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()