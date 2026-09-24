"""Unit tests for PyMuPDF rendering."""

import fitz

from PdfToMarkdown.pdf_pipeline import render_page_to_base64


def test_render_page_to_base64():
    doc = fitz.open()
    page = doc.new_page(width=300, height=300)
    page.insert_text((50, 50), "Test Document Content")

    b64_output = render_page_to_base64(page, dpi=150)
    assert isinstance(b64_output, str)
    assert len(b64_output) > 100
    doc.close()
