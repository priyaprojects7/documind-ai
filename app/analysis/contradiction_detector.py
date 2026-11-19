"""Heuristic detection of potentially opposing claims across two documents."""
import re

NEGATIONS = {"increase": "decrease", "improve": "worsen", "positive": "negative", "effective": "ineffective", "higher": "lower", "significant": "insignificant"}

def detect_contrasts(text_a: str, text_b: str) -> list[str]:
    a = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text_a or "") if len(s.strip()) > 35]
    b = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text_b or "") if len(s.strip()) > 35]
    found = []
    for left in a:
        l = left.lower()
        for right in b:
            r = right.lower()
            shared = set(re.findall(r"[a-z]{5,}", l)) & set(re.findall(r"[a-z]{5,}", r))
            opposing = any((x in l and y in r) or (y in l and x in r) for x,y in NEGATIONS.items())
            if len(shared) >= 3 and opposing:
                found.append(f"Potential contrast (review manually): A: {left[:260]} | B: {right[:260]}")
                if len(found) >= 8: return found
    return found
