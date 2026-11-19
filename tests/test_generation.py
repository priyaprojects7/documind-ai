from dataclasses import replace
from app.generation.answer_generator import generate_answer
import app.generation.answer_generator as generator
from app.utils.config import settings


def test_extracts_answer_without_api_key(monkeypatch):
    monkeypatch.setattr(generator, "settings", replace(settings, openai_api_key=""))
    result = generate_answer("What is reported?", [{"filename":"paper.pdf", "chunk_id":0, "content":"The paper reports improved accuracy.", "score":0.8}])
    assert "improved accuracy" in result.answer
    assert result.citations[0]['label'] == "S1"
