"""Prompt construction for grounded research QA."""
def build_qa_prompt(question: str, sources: list[dict]) -> str:
    evidence = "\n\n".join(f"[{s['label']}] {s['filename']} (chunk {s['chunk_id']}):\n{s['content']}" for s in sources)
    return f"Question: {question}\n\nEvidence:\n{evidence}\n\nAnswer carefully. Separate reported findings from interpretation. Cite factual statements with [S#]. If the evidence does not answer the question, say so."
