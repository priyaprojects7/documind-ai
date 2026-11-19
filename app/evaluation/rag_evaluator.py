"""Evaluate retrieval against the built-in weak-label test set."""
import pandas as pd
from app.evaluation.test_dataset import TEST_QUESTIONS
from app.retrieval.retriever import retrieve

def evaluate_retrieval() -> dict:
    details, hits = [], 0
    for item in TEST_QUESTIONS:
        results = retrieve(item['question'], top_k=5)
        text = " ".join(r['content'].lower() for r in results)
        hit = any(term in text for term in item['expected_terms'])
        hits += int(hit)
        details.append({"Question": item['question'], "Retrieved chunks": len(results), "Expected term found": hit})
    return {"total": len(details), "hit_rate": hits / max(len(details), 1), "details": pd.DataFrame(details)}
