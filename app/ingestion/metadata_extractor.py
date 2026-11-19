"""Lightweight metadata extraction from common paper front-matter patterns."""
import re

def extract_metadata(text: str, filename: str = "paper.pdf") -> dict:
    head = "\n".join(text.splitlines()[:45])
    title = next((line.strip() for line in head.splitlines() if len(line.strip()) > 12 and not line.strip().lower().startswith(("abstract", "arxiv"))), filename.rsplit(".",1)[0])
    abstract_match = re.search(r"(?is)abstract\s*[:\n]\s*(.{80,1800}?)(?=\n\s*(?:1\.?\s*)?(?:introduction|keywords)\b)", text)
    authors = []
    for line in head.splitlines()[1:12]:
        if re.search(r"[A-Z][a-z]+\s+[A-Z][a-z]+", line) and len(line) < 180:
            authors.append(line.strip())
            break
    return {"title": title[:240], "authors": "; ".join(authors), "abstract": abstract_match.group(1).strip() if abstract_match else ""}
