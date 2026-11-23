"""Persistent lightweight vector index stored in SQLite."""
import json
import numpy as np
from app.database.connection import get_connection
from app.ingestion.chunker import TextChunk


def add_document_chunks(document_id: int, filename: str, chunks: list[TextChunk], vectors: np.ndarray):
    if len(chunks) != len(vectors):
        raise ValueError("Every chunk must have exactly one embedding.")
    with get_connection() as conn:
        conn.execute("DELETE FROM chunks WHERE document_id = ?", (document_id,))
        for chunk, vector in zip(chunks, vectors):
            conn.execute("INSERT INTO chunks(document_id, filename, chunk_id, content, start_word, end_word, page_number, embedding) VALUES(?,?,?,?,?,?,?,?)",
                         (document_id, filename, chunk.chunk_id, chunk.text, chunk.start_word, chunk.end_word, chunk.page_number, json.dumps(vector.tolist())))


def all_chunks():
    with get_connection() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM chunks ORDER BY document_id, chunk_id").fetchall()]
