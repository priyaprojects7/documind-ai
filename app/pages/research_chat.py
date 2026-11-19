"""Question answering over indexed papers."""
import streamlit as st
from app.retrieval.retriever import retrieve
from app.generation.answer_generator import generate_answer


def render():
    st.title("Research Chat")
    st.caption("Ask questions across your uploaded papers. Answers include source-level citations.")
    question = st.text_area("Your research question", placeholder="What methods are used to detect distribution shift?")
    if st.button("Find answer", type="primary", disabled=not question.strip()):
        with st.spinner("Searching your library..."):
            passages = retrieve(question, top_k=6)
            if not passages:
                st.warning("No indexed passages found. Upload papers in Document Library first.")
            else:
                result = generate_answer(question, passages)
                st.markdown(result.answer)
                st.subheader("Sources")
                for citation in result.citations:
                    st.markdown(f"- **[{citation['label']}]** {citation['filename']} · chunk {citation['chunk_id']} · relevance {citation['score']:.3f}")
                if result.warnings:
                    st.warning(" ".join(result.warnings))
