# DocuMind AI

DocuMind AI is a local research-paper intelligence workspace for PDF ingestion, semantic search, evidence-grounded question answering, paper comparison, research-gap exploration, and retrieval evaluation.

## Included project archive

The complete project source is available in [`documind-ai.zip`](./documind-ai.zip). Extract it to access the application, tests, documentation, Docker setup, and GitHub Actions workflows.

## Quick start

Requires Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app/main.py
```

Never commit `.env`, API keys, private PDFs, or local databases. The project archive includes `.env.example` only.
