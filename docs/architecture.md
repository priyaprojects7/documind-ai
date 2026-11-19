# Architecture

DocuMind AI is a local-first research-paper assistant. Streamlit provides the user interface. The ingestion pipeline extracts selectable PDF text, cleans it, chunks it, and stores document metadata plus vectors in SQLite. Sentence Transformers produces normalized embeddings when available; a deterministic hashing fallback keeps the app runnable offline. Retrieval ranks chunks by cosine similarity and a lightweight lexical reranker. Answer generation uses OpenAI when `OPENAI_API_KEY` is configured and otherwise returns cited extractive passages.

```text
PDF upload -> PDF loader -> cleaner -> chunker -> embedding model -> SQLite
Question -> query embedding -> similarity search -> reranker -> answer + citations
```

The analysis modules provide transparent heuristics for paper comparison, possible claim contrasts, and candidate gap discovery. These are aids for researcher review, not substitutes for reading the papers.

## Storage and boundaries

SQLite is the default to make local setup simple. The repository interface isolates persistence so a PostgreSQL implementation can replace it later. Uploaded PDFs and the database are local runtime data and are excluded from Git.
