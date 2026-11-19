"""Compare indexed papers on research dimensions."""
import streamlit as st
from app.database.document_repository import list_documents, get_document
from app.analysis.paper_comparator import compare_papers


def render():
    st.title("Paper Comparison")
    docs = list_documents()
    if len(docs) < 2:
        st.info("Upload at least two papers to compare them.")
        return
    labels = {f"{d['title']} ({d['filename']})": d['id'] for d in docs}
    selected = st.multiselect("Choose papers", list(labels), max_selections=5)
    if st.button("Compare papers", type="primary", disabled=len(selected) < 2):
        papers = [get_document(labels[x]) for x in selected]
        result = compare_papers(papers)
        st.dataframe(result, use_container_width=True, hide_index=True)
