# Project Design

## Goal
Help a researcher organize papers, search across them, compare reported methods and findings, and develop evidence-backed questions for further investigation.

## Core workflows
1. Upload a selectable-text PDF and extract page text and basic front-matter metadata.
2. Split text into overlapping chunks and create vector representations.
3. Search the corpus and return source filenames and chunk identifiers.
4. Generate an answer from retrieved evidence, checking citation labels.
5. Compare paper objectives, methods, datasets, and limitations.
6. Inspect possible contrasts and candidate research gaps manually.
7. Run a small weak-label retrieval evaluation.

## Known limits
Scanned PDFs need OCR; metadata extraction is pattern-based; table extraction is a text-layout heuristic; gap and contradiction detection are heuristic; the built-in evaluation set is a smoke test rather than a benchmark. Always verify claims against original papers.
