"""Extract simple text tables from PDF pages when available."""
from io import BytesIO
from pypdf import PdfReader

def extract_tables(pdf_bytes: bytes) -> list[dict]:
    """Return page text blocks that look tabular; full cell extraction needs OCR/layout tooling."""
    reader = PdfReader(BytesIO(pdf_bytes))
    tables = []
    for number, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        candidates = [line for line in lines if line.count("  ") >= 2 or "|" in line or "\t" in line]
        if candidates:
            tables.append({"page": number, "rows": candidates})
    return tables
