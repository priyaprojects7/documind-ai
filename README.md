# DocuMind AI

**DocuMind AI is a local-first research workspace that turns a folder of academic PDFs into a searchable, citable research assistant with persistent chat history.**

Upload papers, ask questions across them, compare methods and findings, inspect candidate research gaps, and evaluate retrieval quality. Research Chat now saves separate conversations, answers, and source citations in SQLite so you can leave a session and return to it later.

## Features

- PDF text extraction and front-matter metadata capture.
- Overlapping text chunking and vector embeddings.
- Persistent local SQLite document, chunk, conversation, and message stores.
- Multiple named Research Chat conversations with saved user questions, answers, and citations.
- Similarity retrieval with lexical reranking.
- Page-level provenance retained during chunking and displayed with retrieved citations.
- Grounded Q&A with source labels and citation validation.
- Paper comparison, candidate gap analysis, and potential claim-contrast detection.
- Retrieval evaluation, Streamlit interface, tests, linting, and Docker setup.

## Quick start

Requires Python 3.11+. From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app/main.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501). Upload a selectable-text PDF in Document Library. The first Sentence Transformers run may download the embedding model. If it cannot load, a deterministic hashing fallback is used. Add an OpenAI API key to `.env` to enable synthesized answers; without it, the app returns relevant passages in extractive mode. Restart Streamlit after changing `.env`.

## Research Chat history

- Start a new conversation with **＋ New chat**.
- Switch between previous conversations using **Conversation history**.
- User questions, assistant answers, and citation metadata are stored in the local SQLite database.
- The first question becomes the conversation title; you can continue the same thread after switching pages or restarting the local app.

Existing DocuMind databases are upgraded automatically when the app starts. The new tables are additive; existing papers and indexed chunks are retained.

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

## Important limitations

Scanned PDFs require OCR before upload. Table extraction and metadata extraction use lightweight heuristics. Contradiction and research-gap outputs are suggestions for manual review, not verified scientific conclusions. The included retrieval evaluation uses a small weak-label smoke-test set, not a validated benchmark.

## Security and deployment

Never commit `.env`, API keys, private PDFs, or the local database. Review paper licenses before sharing extracted content.

This repository is local-first and currently has no user authentication or per-user data isolation. Do not deploy it as a public multi-user service with private research papers until authentication, tenant isolation, and persistent private storage are implemented. The local SQLite chat history is intended for a single local user.
