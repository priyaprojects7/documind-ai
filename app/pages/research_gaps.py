"""Identify candidate research gaps from the indexed corpus."""
import streamlit as st
from app.database.document_repository import list_documents, get_document
from app.analysis.gap_analyzer import analyze_gaps


def render():
    st.title("Research Gaps")
    docs = list_documents()
    if not docs:
        st.info("Upload papers before running a gap analysis.")
        return
    selected = st.multiselect("Include papers", [d['filename'] for d in docs], default=[d['filename'] for d in docs])
    if st.button("Analyze research gaps", type="primary", disabled=not selected):
        papers = [get_document(d['id']) for d in docs if d['filename'] in selected]
        gaps = analyze_gaps(papers)
        if not gaps:
            st.info("The available text did not contain enough recurring themes to suggest candidate gaps.")
        for gap in gaps:
            with st.expander(gap['title']):
                st.write(gap['reason'])
                st.caption("Evidence: " + "; ".join(gap['evidence']))
                st.caption("Treat these as hypotheses to validate, not established research gaps.")
