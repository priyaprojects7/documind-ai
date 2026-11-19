# DocuMind AI

DocuMind AI is a local research-paper intelligence workspace. Upload PDFs, search across papers, ask evidence-grounded questions, compare papers, inspect possible research gaps, and run a basic retrieval evaluation.

## Features
- PDF text extraction and front-matter metadata capture
- Overlapping text chunking and vector embeddings
- Persistent local SQLite document and chunk store
- Similarity retrieval with lexical reranking
- Grounded Q&A with source labels and citation validation
- Paper comparison, candidate gap analysis, and potential claim-contrast detection
- Streamlit interface, tests, linting, and Docker setup

## Quick start

Requires Python 3.11+. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app/main.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501). Upload a selectable-text PDF in Document Library. The first Sentence Transformers run may download the embedding model. If it cannot load, a deterministic hashing fallback is used. Add an OpenAI API key to `.env` to enable synthesized answers; without it, the app returns relevant passages in extractive mode. Restart Streamlit after changing `.env`.

## Docker

```bash
cp .env.example .env
docker compose up --build
```

## Tests and lint

```bash
pytest -q
ruff check app tests
```

## Project structure

```text
documind-ai/
├── app/                  # UI, ingestion, embeddings, retrieval, generation, analysis
├── tests/                # automated tests
├── data/                 # local runtime data (ignored by Git)
├── notebooks/            # exploration notebook
├── docs/                 # architecture and design notes
├── .github/workflows/    # CI tests and lint
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── README.md
└── LICENSE
```

The detailed module-by-module tree is retained in the repository.

## Important limitations
Scanned PDFs require OCR before upload. Table extraction and metadata extraction use lightweight heuristics. Contradiction and research-gap outputs are suggestions for manual review, not verified scientific conclusions. The included retrieval evaluation uses a small weak-label smoke-test set, not a validated benchmark.

## Security
Never commit `.env`, API keys, private PDFs, or the local database. Review paper licenses before sharing extracted content.
