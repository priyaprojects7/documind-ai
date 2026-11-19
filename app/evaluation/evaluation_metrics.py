"""Simple information retrieval metrics."""
def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    if not relevant: return 0.0
    return len(set(retrieved[:k]) & relevant) / len(relevant)

def reciprocal_rank(retrieved: list[str], relevant: set[str]) -> float:
    for rank, item in enumerate(retrieved, 1):
        if item in relevant: return 1.0 / rank
    return 0.0
