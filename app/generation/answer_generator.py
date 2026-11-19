"""Generate grounded answers; OpenAI is optional and extractive fallback is always available."""
from dataclasses import dataclass
from app.generation.prompt_templates import build_qa_prompt
from app.generation.citation_checker import validate_citations
from app.utils.config import settings

@dataclass
class AnswerResult:
    answer: str
    citations: list[dict]
    warnings: list[str]


def generate_answer(question: str, passages: list[dict]) -> AnswerResult:
    sources = [{"label": f"S{i+1}", "filename": p['filename'], "chunk_id": p['chunk_id'], "score": p.get('score', 0), "content": p['content']} for i,p in enumerate(passages)]
    warnings = []
    answer = ""
    if settings.openai_api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.openai_api_key)
            response = client.chat.completions.create(model=settings.openai_model, temperature=0.1,
                messages=[{"role":"system","content":"Answer only from supplied evidence. Cite each factual claim using [S1] style. Say when evidence is insufficient."},
                          {"role":"user","content":build_qa_prompt(question, sources)}])
            answer = response.choices[0].message.content or ""
        except Exception as exc:
            warnings.append(f"LLM request failed; using extractive fallback ({type(exc).__name__}).")
    if not answer:
        best = sources[:3]
        answer = "The most relevant passages in your library are:\n\n" + "\n\n".join(f"{s['content'][:700]} [{s['label']}]" for s in best)
        warnings.append("Extractive mode is active. Configure OPENAI_API_KEY for synthesized answers.")
    checked = validate_citations(answer, sources)
    if checked['unknown']:
        warnings.append("The answer contains citation labels that do not match retrieved sources.")
    cited = [s for s in sources if s['label'] in checked['valid']]
    if not cited:
        cited = sources[:3]
    return AnswerResult(answer, cited, warnings)
