"""
downloader.py
Utility for extracting text content from uploaded PDFs.
"""

import io

import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
from pypdf import PdfReader


def extract_text_from_pdf(file, ocr_lang="fra") -> str:
    """
    Extract text from a PDF file.
    Handles both:
        - Normal text PDFs
        - Scanned PDFs (images) using OCR
    Args:
        file: a file-like object (BytesIO or UploadedFile)
        ocr_lang: language for OCR (default: 'fra' for French)
    Returns:
        str: extracted text
    """
    # Read file content once
    file_content = file.read()

    try:
        reader = PdfReader(io.BytesIO(file_content))
        text = ""

        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""

            # Check if meaningful text was extracted
            if len(page_text.strip()) > 50:
                text += f"\n--- Page {i+1} ---\n{page_text}"
            else:
                # Fallback to OCR for this page
                try:
                    images = convert_from_bytes(
                        file_content, first_page=i + 1, last_page=i + 1, dpi=300
                    )
                    if images:
                        ocr_text = pytesseract.image_to_string(images[0], lang=ocr_lang)
                        text += f"\n--- Page {i+1} (OCR) ---\n{ocr_text}"
                except Exception as e:
                    text += f"\n--- Page {i+1} (Error) ---\nCould not extract text: {str(e)}\n"

        return text.strip()

    except Exception as e:
        return f"Error processing PDF: {str(e)}"
