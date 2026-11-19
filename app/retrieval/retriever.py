"""Cosine-similarity retrieval over stored chunk embeddings."""
import json
import numpy as np
from app.embeddings.embedding_model import embed_texts
from app.retrieval.vector_store import all_chunks
from app.retrieval.reranker import rerank


def retrieve(query: str, top_k: int = 5, document_ids: list[int] | None = None) -> list[dict]:
    rows = all_chunks()
    if document_ids is not None:
        rows = [r for r in rows if r['document_id'] in document_ids]
    if not rows or not query.strip():
        return []
    matrix = np.asarray([json.loads(r['embedding']) for r in rows], dtype=np.float32)
    q = embed_texts([query])[0]
    scores = matrix @ q
    ranked = sorted(zip(rows, scores), key=lambda x: float(x[1]), reverse=True)[:max(top_k * 3, top_k)]
    results = [{**row, 'score': float(score)} for row, score in ranked]
    return rerank(query, results)[:top_k]
