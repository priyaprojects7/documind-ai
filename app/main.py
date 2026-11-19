"""Streamlit entry point for DocuMind AI."""
import streamlit as st
from app.pages import document_library, research_chat, paper_comparison, research_gaps, document_comparison, evaluation
from app.database.connection import init_db
from app.utils.config import settings

st.set_page_config(page_title="DocuMind AI", page_icon="📚", layout="wide")
init_db()
st.sidebar.title("DocuMind AI")
st.sidebar.caption("Research paper intelligence workspace")
PAGES = {
    "Document Library": document_library.render,
    "Research Chat": research_chat.render,
    "Paper Comparison": paper_comparison.render,
    "Research Gaps": research_gaps.render,
    "Document Comparison": document_comparison.render,
    "Evaluation": evaluation.render,
}
choice = st.sidebar.radio("Workspace", list(PAGES))
st.sidebar.divider()
st.sidebar.caption(f"Embedding model: {settings.embedding_model}")
PAGES[choice]()
