"""CRUD operations for research paper records."""
from app.database.connection import get_connection, init_db

def save_document(filename: str, metadata: dict, text: str, page_count: int) -> int:
    init_db()
    with get_connection() as conn:
        existing = conn.execute("SELECT id FROM documents WHERE filename=?", (filename,)).fetchone()
        if existing:
            doc_id = existing['id']
            conn.execute("UPDATE documents SET title=?, authors=?, abstract=?, full_text=?, page_count=?, created_at=CURRENT_TIMESTAMP WHERE id=?",
                         (metadata.get('title'), metadata.get('authors'), metadata.get('abstract'), text, page_count, doc_id))
            return doc_id
        cur = conn.execute("INSERT INTO documents(filename,title,authors,abstract,full_text,page_count) VALUES(?,?,?,?,?,?)",
                           (filename, metadata.get('title'), metadata.get('authors'), metadata.get('abstract'), text, page_count))
        return cur.lastrowid

def list_documents() -> list[dict]:
    init_db()
    with get_connection() as conn:
        return [dict(r) for r in conn.execute("SELECT id, filename, title, authors, abstract, page_count, substr(full_text,1,500) AS text_preview, created_at FROM documents ORDER BY created_at DESC").fetchall()]

def get_document(document_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM documents WHERE id=?", (document_id,)).fetchone()
        return dict(row) if row else None
