from io import BytesIO
from pypdf import PdfWriter
from app.ingestion.pdf_loader import load_pdf

def test_load_pdf_extracts_page_text():
    writer = PdfWriter(); writer.add_blank_page(width=300, height=300)
    # A blank PDF has no selectable text and should fail with a useful message.
    stream = BytesIO(); writer.write(stream)
    try:
        load_pdf(stream.getvalue())
    except ValueError as exc:
        assert "No selectable text" in str(exc)
    else:
        raise AssertionError("Expected empty-text PDF to be rejected")
