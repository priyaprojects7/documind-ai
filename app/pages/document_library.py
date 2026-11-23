"""Upload, index, and browse research papers."""
import streamlit as st
from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import chunk_text
from app.ingestion.metadata_extractor import extract_metadata
from app.database.document_repository import save_document, list_documents, get_document
from app.embeddings.embedding_model import embed_texts
from app.retrieval.vector_store import add_document_chunks


def render():
    st.title("Document Library")
    st.write("Upload research PDFs to extract text, metadata, and searchable passages.")
    uploads = st.file_uploader("Upload PDF papers", type=["pdf"], accept_multiple_files=True)
    if uploads and st.button("Process selected papers", type="primary"):
        for upload in uploads:
            try:
                raw = upload.getvalue()
                pages = load_pdf(raw)
                full_text = "\n".join(p.text for p in pages)
                meta = extract_metadata(full_text, upload.name)
                chunks = []
                next_chunk_id = 0
                for page in pages:
                    page_chunks = chunk_text(
                        page.text, page_number=page.page_number,
                        start_chunk_id=next_chunk_id,
                    )
                    chunks.extend(page_chunks)
                    next_chunk_id += len(page_chunks)
                if not chunks:
                    raise ValueError("No text chunks could be created from this PDF.")
                doc_id = save_document(upload.name, meta, full_text, len(pages))
                vectors = embed_texts([c.text for c in chunks])
                add_document_chunks(doc_id, upload.name, chunks, vectors)
                st.success(f"Indexed {upload.name}: {len(pages)} pages, {len(chunks)} chunks. Source-page references are now retained.")
            except Exception as exc:
                st.error(f"Could not process {upload.name}: {exc}")
    docs = list_documents()
    st.subheader(f"Your papers ({len(docs)})")
    if not docs:
        st.info("No papers yet. Upload a PDF to get started.")
    for doc in docs:
        with st.expander(f"{doc['title']} · {doc['filename']}"):
            st.write(f"**Authors:** {doc.get('authors') or 'Not detected'}")
            st.write(f"**Pages:** {doc.get('page_count', 0)}")
            st.write((doc.get('abstract') or doc.get('text_preview') or "No preview available")[:1200])
