"""Suggest candidate underexplored themes from paper abstracts and limitations."""
import re
from collections import Counter, defaultdict
STOP = {"about","after","again","against","being","between","could","their","there","these","those","which","while","where","would","should","using","based","from","with","that","this","have","were","they","into","than","also","such","paper","study","result","results","method","methods"}

def analyze_gaps(papers: list[dict], min_frequency: int = 2) -> list[dict]:
    """Suggest recurring themes with uneven coverage; this is not proof of a gap."""
    if min_frequency < 1:
        raise ValueError("min_frequency must be at least 1")
    if len(papers) < 2:
        return []
    counts, evidence = Counter(), defaultdict(list)
    for paper in papers:
        source = (paper.get('abstract') or paper.get('text','')[:2500]).lower()
        terms = set(re.findall(r"[a-z][a-z-]{4,}", source)) - STOP
        for term in terms:
            counts[term] += 1
            evidence[term].append(paper.get('filename', paper.get('title','paper')))
    candidates = [(term, n) for term,n in counts.items() if min_frequency <= n < len(papers)]
    candidates.sort(key=lambda x: (len(papers)-x[1], -len(x[0])))
    return [{"title": f"Investigate {term.replace('-', ' ')}", "reason": f"The term appears in {n} of {len(papers)} selected papers and is absent from {len(papers) - n}. This is a keyword-level signal only; inspect the full methods, results and limitations before treating it as a research gap.", "evidence": evidence[term], "paper_count": n, "corpus_size": len(papers)} for term,n in candidates[:10]]
