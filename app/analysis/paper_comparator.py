"""Extract comparable paper attributes into a tabular result."""
import re
import pandas as pd

KEYWORDS = {"objective": ["we propose", "this paper", "aim"], "method": ["method", "model", "algorithm", "framework"], "dataset": ["dataset", "benchmark", "corpus"], "limitations": ["limitation", "future work", "however"]}

def _extract(text: str, terms: list[str]) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text or "")
    hits = [s.strip() for s in sentences if any(t in s.lower() for t in terms)]
    return " ".join(hits[:2])[:500] or "Not clearly identified in extracted text"

def compare_papers(papers: list[dict]) -> pd.DataFrame:
    rows = []
    for p in papers:
        text = p.get('text', '')
        row = {"Paper": p.get('title') or p.get('filename')}
        for key, terms in KEYWORDS.items(): row[key.title()] = _extract(text, terms)
        rows.append(row)
    return pd.DataFrame(rows)
