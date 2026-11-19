"""Extract page text from PDF bytes."""
from dataclasses import dataclass
from io import BytesIO
from pypdf import PdfReader

@dataclass
class PDFPage:
    page_number: int
    text: str


def load_pdf(source: bytes) -> list[PDFPage]:
    if not source:
        raise ValueError("The uploaded PDF is empty.")
    reader = PdfReader(BytesIO(source))
    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception as exc:
            raise ValueError("Encrypted PDFs are not supported unless they can be opened without a password.") from exc
    pages = [PDFPage(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]
    if not any(p.text.strip() for p in pages):
        raise ValueError("No selectable text found. Scanned PDFs need OCR before ingestion.")
    return pages
