"""Create a concise extractive summary from a paper."""
import re

def summarize(text: str, max_sentences: int = 5) -> str:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text or "") if len(s.strip()) > 35]
    if not sentences: return "No readable text was extracted."
    keywords = {"propose", "find", "show", "result", "method", "limitation", "conclude", "performance"}
    ranked = sorted(enumerate(sentences), key=lambda x: (sum(k in x[1].lower() for k in keywords), -x[0]), reverse=True)
    chosen = sorted(i for i,_ in ranked[:max_sentences])
    return " ".join(sentences[i] for i in chosen)
