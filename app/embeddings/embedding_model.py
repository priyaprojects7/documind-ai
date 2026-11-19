"""Sentence-transformer embeddings with deterministic local fallback."""
import hashlib
import numpy as np
from app.utils.config import settings

_model = None

def _load_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer(settings.embedding_model)
        except Exception:
            _model = False
    return _model


def embed_texts(texts: list[str]) -> np.ndarray:
    if not texts:
        return np.empty((0, 384), dtype=np.float32)
    model = _load_model()
    if model:
        return np.asarray(model.encode(texts, normalize_embeddings=True), dtype=np.float32)
    # Hashing fallback keeps tests and first-run use offline; semantic quality is lower.
    vectors = np.zeros((len(texts), 384), dtype=np.float32)
    for row, text in enumerate(texts):
        for token in text.lower().split():
            digest = hashlib.blake2b(token.encode(), digest_size=8).digest()
            index = int.from_bytes(digest[:4], "little") % 384
            vectors[row, index] += 1.0 if digest[4] % 2 else -1.0
        norm = np.linalg.norm(vectors[row])
        if norm:
            vectors[row] /= norm
    return vectors
