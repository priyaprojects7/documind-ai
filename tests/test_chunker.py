import pytest
from app.ingestion.chunker import chunk_text

def test_chunk_overlap_and_order():
    chunks = chunk_text(" ".join(f"w{i}" for i in range(11)), chunk_size=5, overlap=2)
    assert [c.text for c in chunks] == ["w0 w1 w2 w3 w4", "w3 w4 w5 w6 w7", "w6 w7 w8 w9 w10"]

def test_invalid_overlap():
    with pytest.raises(ValueError): chunk_text("a b", chunk_size=3, overlap=3)
