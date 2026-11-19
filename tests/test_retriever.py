from app.retrieval.reranker import rerank

def test_reranker_prefers_lexical_overlap():
    rows = [{"content":"unrelated material", "score":0.8}, {"content":"machine learning model evaluation", "score":0.5}]
    assert rerank("machine learning model", rows)[0]['content'].startswith("machine")
