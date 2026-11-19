from app.embeddings.embedding_model import embed_texts
import app.embeddings.embedding_model as embedding_model


def test_embedding_shape_and_normalization(monkeypatch):
    monkeypatch.setattr(embedding_model, "_load_model", lambda: False)
    vectors = embed_texts(["research paper", "machine learning"])
    assert vectors.shape == (2, 384)
    assert abs(float((vectors[0] ** 2).sum()) - 1.0) < 1e-5
