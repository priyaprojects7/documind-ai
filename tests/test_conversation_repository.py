import json
from app.database.conversation_repository import (
    create_conversation, get_messages, list_conversations, rename_conversation, save_message,
)
import app.database.connection as connection


def test_conversation_history_persists_and_can_be_reloaded(tmp_path, monkeypatch):
    monkeypatch.setattr(connection, "_db_path", lambda: tmp_path / "test.db")
    conversation_id = create_conversation()
    save_message(conversation_id, "user", "What is the paper's main method?")
    citations = [{"label": "S1", "filename": "paper.pdf", "chunk_id": 2, "score": 0.91}]
    save_message(conversation_id, "assistant", "It uses a graph model. [S1]", citations)
    rename_conversation(conversation_id, "Main method discussion")

    history = get_messages(conversation_id)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["content"] == "It uses a graph model. [S1]"
    assert json.loads(history[1]["citations_json"]) == citations
    assert list_conversations()[0]["title"] == "Main method discussion"


def test_conversation_sessions_are_separate(tmp_path, monkeypatch):
    monkeypatch.setattr(connection, "_db_path", lambda: tmp_path / "test.db")
    first = create_conversation("First")
    second = create_conversation("Second")
    save_message(first, "user", "Question one")
    assert len(get_messages(first)) == 1
    assert get_messages(second) == []
