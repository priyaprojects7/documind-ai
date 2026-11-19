"""Check that generated citation labels refer to retrieved passages."""
import re

def validate_citations(answer: str, sources: list[dict]) -> dict:
    used = set(re.findall(r"\[(S\d+)\]", answer))
    known = {s['label'] for s in sources}
    return {"valid": sorted(used & known), "unknown": sorted(used - known), "missing": not bool(used)}
