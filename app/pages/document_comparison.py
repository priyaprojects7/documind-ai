"""Side-by-side comparison of two full document records."""
import streamlit as st
from app.database.document_repository import list_documents, get_document
from app.analysis.contradiction_detector import detect_contrasts


def render():
    st.title("Document Comparison")
    docs = list_documents()
    if len(docs) < 2:
        st.info("Upload at least two papers to compare their claims and limitations.")
        return
    labels = {d['filename']: d['id'] for d in docs}
    left = st.selectbox("Paper A", list(labels))
    right = st.selectbox("Paper B", [x for x in labels if x != left])
    if st.button("Compare claims", type="primary"):
        a, b = get_document(labels[left]), get_document(labels[right])
        contrasts = detect_contrasts(a.get('full_text') or a.get('text',''), b.get('full_text') or b.get('text',''))
        if contrasts:
            for item in contrasts:
                st.markdown(f"- {item}")
        else:
            st.info("No direct opposing statements were detected with the current heuristic. This does not prove the papers agree.")
