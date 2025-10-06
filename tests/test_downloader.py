"""
test_downloader.py
Simple tests for PDF text extraction function
"""

import io
import pytest
from pypdf import PdfWriter
from project_summarizer.utils.downloader import extract_text_from_pdf


def create_fake_pdf(text: str) -> io.BytesIO:
    """Create a fake PDF with text for testing purposes."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, text)
    c.save()
    buffer.seek(0)
    return buffer


class TestExtractTextFromPDF:
    """Test suite for extract_text_from_pdf function"""
    
    def test_extract_simple_text(self):
        """Test 1: Verify that simple text can be extracted"""
        # ARRANGE (Setup)
        fake_pdf = create_fake_pdf("Hello World")
        
        # ACT (Execute)
        result = extract_text_from_pdf(fake_pdf)
        
        # ASSERT (Verify)
        assert "Hello World" in result
        assert isinstance(result, str)
    
    def test_extract_returns_string(self):
        """Test 2: Verify that the function returns a string"""
        fake_pdf = create_fake_pdf("Test")
        result = extract_text_from_pdf(fake_pdf)
        
        assert isinstance(result, str)
    
    def test_extract_strips_whitespace(self):
        """Test 3: Verify that whitespace is stripped"""
        fake_pdf = create_fake_pdf("   Text with spaces   ")
        result = extract_text_from_pdf(fake_pdf)
        
        # Result should not start or end with spaces
        assert result == result.strip()
    
    def test_empty_pdf(self):
        """Test 4: Verify behavior with an empty PDF"""
        fake_pdf = create_fake_pdf("")
        result = extract_text_from_pdf(fake_pdf)
        
        # Empty PDF should return empty string
        assert result == ""