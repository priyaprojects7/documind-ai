"""Small lexical reranker to refine embedding retrieval order."""
import re

def rerank(query: str, results: list[dict]) -> list[dict]:
    terms = set(re.findall(r"[a-z0-9]{3,}", query.lower()))
    for item in results:
        words = set(re.findall(r"[a-z0-9]{3,}", item['content'].lower()))
        overlap = len(terms & words) / max(len(terms), 1)
        item['rerank_score'] = 0.75 * item.get('score', 0.0) + 0.25 * overlap
    return sorted(results, key=lambda x: x['rerank_score'], reverse=True)
