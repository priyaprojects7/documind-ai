"""Suggest candidate underexplored themes from paper abstracts and limitations."""
import re
from collections import Counter, defaultdict
STOP = {"about","after","again","against","being","between","could","their","there","these","those","which","while","where","would","should","using","based","from","with","that","this","have","were","they","into","than","also","such","paper","study","result","results","method","methods"}

def analyze_gaps(papers: list[dict], min_frequency: int = 2) -> list[dict]:
    counts, evidence = Counter(), defaultdict(list)
    for paper in papers:
        source = (paper.get('abstract') or paper.get('text','')[:2500]).lower()
        terms = set(re.findall(r"[a-z][a-z-]{4,}", source)) - STOP
        for term in terms:
            counts[term] += 1
            evidence[term].append(paper.get('filename', paper.get('title','paper')))
    candidates = [(term, n) for term,n in counts.items() if 1 < n < len(papers)]
    candidates.sort(key=lambda x: (len(papers)-x[1], -len(x[0])))
    return [{"title": f"Investigate {term.replace('-', ' ')}", "reason": f"The term appears in {n} of {len(papers)} selected papers. It may represent a theme that receives uneven coverage; inspect full methods and limitations before treating it as a gap.", "evidence": evidence[term]} for term,n in candidates[:10]]
