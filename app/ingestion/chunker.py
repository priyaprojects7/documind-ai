"""Split text into overlapping word-window chunks while retaining source page."""
from dataclasses import dataclass
from app.ingestion.text_cleaner import clean_text


@dataclass
class TextChunk:
    chunk_id: int
    text: str
    start_word: int
    end_word: int
    page_number: int | None = None


def chunk_text(
    text: str, chunk_size: int = 220, overlap: int = 40,
    page_number: int | None = None, start_chunk_id: int = 0,
) -> list[TextChunk]:
    if chunk_size < 1 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Require chunk_size > overlap >= 0.")
    words = clean_text(text).split()
    chunks, start, idx = [], 0, start_chunk_id
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(TextChunk(idx, " ".join(words[start:end]), start, end, page_number))
        if end == len(words):
            break
        start = end - overlap
        idx += 1
    return chunks
