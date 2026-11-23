"""Persistent, multi-session question answering over indexed papers."""
import json
import streamlit as st
from app.retrieval.retriever import retrieve
from app.generation.answer_generator import generate_answer
from app.database.conversation_repository import (
    create_conversation, get_messages, list_conversations, rename_conversation, save_message,
)


def _render_message(message):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        citations = json.loads(message.get("citations_json") or "[]")
        if citations:
            with st.expander(f"Sources ({len(citations)})"):
                for citation in citations:
                    st.markdown(
                        f"- **[{citation.get('label', 'Source')}]** "
                        f"{citation.get('filename', 'Unknown file')} · "
                        f"page {citation.get('page_number') or 'not recorded'} · "
                        f"chunk {citation.get('chunk_id', '?')} · "
                        f"relevance {citation.get('score', 0):.3f}"
                    )


def render():
    st.title("Research Chat")
    st.caption("Ask questions across your indexed papers. Conversations and citations are saved locally.")

    conversations = list_conversations()
    if "documind_conversation_id" not in st.session_state:
        st.session_state.documind_conversation_id = (
            conversations[0]["id"] if conversations else create_conversation()
        )
    known_ids = {item["id"] for item in conversations}
    if st.session_state.documind_conversation_id not in known_ids:
        conversations = list_conversations()
        known_ids = {item["id"] for item in conversations}
        if st.session_state.documind_conversation_id not in known_ids:
            st.session_state.documind_conversation_id = (
                conversations[0]["id"] if conversations else create_conversation()
            )

    left, right = st.columns([1, 4])
    with left:
        if st.button("＋ New chat", use_container_width=True):
            new_id = create_conversation()
            st.session_state.documind_conversation_id = new_id
            st.session_state.documind_history_selector = new_id
            st.rerun()

    conversations = list_conversations()
    if conversations:
        ids = [item["id"] for item in conversations]
        labels = {item["id"]: f"{item['title']} · {item['message_count']} messages" for item in conversations}
        active_id = st.session_state.documind_conversation_id
        if active_id not in ids:
            active_id = ids[0]
            st.session_state.documind_conversation_id = active_id
        with right:
            selected_id = st.selectbox(
                "Conversation history",
                ids,
                index=ids.index(active_id),
                format_func=lambda value: labels.get(value, "Research chat"),
                key="documind_history_selector",
            )
        if selected_id != st.session_state.documind_conversation_id:
            st.session_state.documind_conversation_id = selected_id
            st.rerun()

    active_id = st.session_state.documind_conversation_id
    messages = get_messages(active_id)
    if not messages:
        st.info("Start a conversation. Your questions, answers, and source citations will remain in History.")
    for message in messages:
        _render_message(message)

    question = st.chat_input("Ask a question about your research papers...")
    if question and question.strip():
        clean_question = question.strip()
        save_message(active_id, "user", clean_question)
        if len(messages) == 0:
            rename_conversation(active_id, clean_question[:70])
        with st.chat_message("user"):
            st.markdown(clean_question)
        with st.chat_message("assistant"):
            with st.spinner("Searching your library and checking sources..."):
                passages = retrieve(clean_question, top_k=6)
                if not passages:
                    answer_text = "I couldn't find indexed passages for this question. Upload papers in Document Library first."
                    citations = []
                    warnings = []
                else:
                    result = generate_answer(clean_question, passages)
                    answer_text = result.answer
                    citations = result.citations
                    warnings = result.warnings
            st.markdown(answer_text)
            if citations:
                with st.expander(f"Sources ({len(citations)})"):
                    for citation in citations:
                        st.markdown(
                            f"- **[{citation['label']}]** {citation['filename']} · "
                            f"chunk {citation['chunk_id']} · relevance {citation['score']:.3f}"
                        )
            if warnings:
                for warning in warnings:
                    st.warning(warning)
        save_message(active_id, "assistant", answer_text, citations)
        st.rerun()
