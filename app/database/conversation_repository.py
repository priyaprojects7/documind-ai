"""Persistent CRUD operations for Research Chat conversations."""
import uuid
from app.database.connection import get_connection, init_db


def create_conversation(title: str = "New research chat") -> str:
    init_db()
    conversation_id = str(uuid.uuid4())
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO chat_conversations(id, title) VALUES(?, ?)",
            (conversation_id, title.strip() or "New research chat"),
        )
    return conversation_id


def list_conversations() -> list[dict]:
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT c.id, c.title, c.created_at, c.updated_at,
                      COUNT(m.id) AS message_count
               FROM chat_conversations c
               LEFT JOIN chat_messages m ON m.conversation_id = c.id
               GROUP BY c.id
               ORDER BY c.updated_at DESC, c.created_at DESC"""
        ).fetchall()
        return [dict(row) for row in rows]


def get_messages(conversation_id: str) -> list[dict]:
    init_db()
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT id, conversation_id, role, content, citations_json, created_at
               FROM chat_messages WHERE conversation_id = ? ORDER BY id""",
            (conversation_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def save_message(conversation_id: str, role: str, content: str, citations: list[dict] | None = None):
    if role not in {"user", "assistant", "system"}:
        raise ValueError("Unsupported message role")
    init_db()
    import json
    with get_connection() as conn:
        exists = conn.execute(
            "SELECT id FROM chat_conversations WHERE id = ?", (conversation_id,)
        ).fetchone()
        if not exists:
            raise ValueError("Conversation does not exist")
        conn.execute(
            """INSERT INTO chat_messages(conversation_id, role, content, citations_json)
               VALUES(?, ?, ?, ?)""",
            (conversation_id, role, content, json.dumps(citations or [])),
        )
        conn.execute(
            "UPDATE chat_conversations SET updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (conversation_id,),
        )


def rename_conversation(conversation_id: str, title: str):
    init_db()
    with get_connection() as conn:
        conn.execute(
            "UPDATE chat_conversations SET title=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (title.strip()[:100] or "Research chat", conversation_id),
        )
