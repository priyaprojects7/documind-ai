# DocuMind AI

DocuMind AI is a local research-paper intelligence workspace for PDF ingestion, semantic search, evidence-grounded question answering, paper comparison, research-gap exploration, and retrieval evaluation.

## Restore the source archive

The complete project source is stored in five ordered Base64 parts in this repository. After cloning the repository, run:

```bash
python3 -c "import base64,pathlib; parts=sorted(pathlib.Path('.').glob('documind-ai-source.tar.gz.b64.*')); pathlib.Path('documind-ai-source.tar.gz').write_bytes(base64.b64decode(''.join(p.read_text() for p in parts)))"
tar -xzf documind-ai-source.tar.gz
cd documind-ai
```

The archive contains the application, tests, documentation, Docker setup, notebooks, and GitHub Actions workflows.

## Quick start

Requires Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app/main.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501). Upload a selectable-text PDF in Document Library. The first Sentence Transformers run may download the embedding model. If it cannot load, a deterministic hashing fallback is used. Add an OpenAI API key to `.env` to enable synthesized answers; without it, the app returns relevant passages in extractive mode.

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

## Security and limitations

Never commit `.env`, API keys, private PDFs, or the local database. The source archive includes `.env.example` only. Review paper licenses before sharing extracted content.

Scanned PDFs require OCR before upload. Table and metadata extraction use lightweight heuristics. Research-gap and contradiction outputs are suggestions for manual review, not verified scientific conclusions.
