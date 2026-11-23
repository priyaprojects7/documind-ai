from app.analysis.gap_analyzer import analyze_gaps


def test_gap_candidates_respect_min_frequency_and_report_coverage():
    papers = [
        {"filename": "a.pdf", "abstract": "Graph neural networks improve prediction."},
        {"filename": "b.pdf", "abstract": "Graph neural networks support classification."},
        {"filename": "c.pdf", "abstract": "Computer vision supports classification."},
    ]
    results = analyze_gaps(papers, min_frequency=2)
    graph = next(item for item in results if item["title"] == "Investigate graph")
    assert graph["paper_count"] == 2
    assert graph["corpus_size"] == 3
    assert "a.pdf" in graph["evidence"]
    assert "b.pdf" in graph["evidence"]


def test_gap_analysis_requires_at_least_two_papers():
    assert analyze_gaps([{"filename": "one.pdf", "abstract": "graph neural networks"}]) == []
