"""Run the small built-in retrieval evaluation set."""
import streamlit as st
from app.evaluation.rag_evaluator import evaluate_retrieval


def render():
    st.title("Evaluation")
    st.write("Measure whether known evaluation questions retrieve their expected source terms.")
    if st.button("Run retrieval evaluation", type="primary"):
        results = evaluate_retrieval()
        st.metric("Hit rate", f"{results['hit_rate']:.1%}")
        st.metric("Questions evaluated", results['total'])
        st.dataframe(results['details'], use_container_width=True, hide_index=True)
