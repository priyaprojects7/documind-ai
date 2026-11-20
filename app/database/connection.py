"""SQLite connection and schema initialization; PostgreSQL can be added behind this interface."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from app.utils.config import settings


def _db_path():
    path = Path(settings.database_url.replace("sqlite:///", ""))
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


@contextmanager
def get_connection():
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS documents ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL, "
            "title TEXT, authors TEXT, abstract TEXT, full_text TEXT, "
            "page_count INTEGER DEFAULT 0, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS chunks ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE, "
            "filename TEXT NOT NULL, chunk_id INTEGER NOT NULL, content TEXT NOT NULL, "
            "start_word INTEGER, end_word INTEGER, embedding TEXT NOT NULL, "
            "UNIQUE(document_id, chunk_id))"
        )
        # Safe additive migration: existing DocuMind databases gain chat history tables.
        conn.execute(
            "CREATE TABLE IF NOT EXISTS chat_conversations ("
            "id TEXT PRIMARY KEY, title TEXT NOT NULL DEFAULT 'New research chat', "
            "created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            "updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )
        conn.execute(
            "CREATE TABLE IF NOT EXISTS chat_messages ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "conversation_id TEXT NOT NULL REFERENCES chat_conversations(id) ON DELETE CASCADE, "
            "role TEXT NOT NULL CHECK(role IN ('user','assistant','system')), "
            "content TEXT NOT NULL, citations_json TEXT NOT NULL DEFAULT '[]', "
            "created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_chat_messages_conversation "
            "ON chat_messages(conversation_id, id)"
        )
