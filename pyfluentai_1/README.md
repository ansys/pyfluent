# pyfluentai

A prototype in-house AI chatbot for answering user queries about [PyFluent](https://fluent.docs.pyansys.com/), built on a RAG (Retrieval-Augmented Generation) architecture using [LlamaIndex](https://www.llamaindex.ai/) and [Ollama](https://ollama.com/).

## Architecture

The system follows a standard RAG pipeline:

1. **Ingestion** — PyFluent documentation (RST source files) is loaded, chunked, and embedded into a local vector index.
2. **Retrieval** — user queries are embedded and matched against the index via similarity search to find the most relevant documentation sections.
3. **Generation** — retrieved sections are passed as context to a locally-running LLM via Ollama, which generates the final answer.

Embeddings are generated locally using [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) via HuggingFace, with no OpenAI dependency.

## Project structure

```
pyfluentai/
├── docsource/          # Trimmed PyFluent RST documentation (non-generated files only)
├── examples/           # Exploratory scripts used during development
│   └── pyfluent_index/ # Persisted LlamaIndex vector store (generated, not committed)
├── src/
│   └── pyfluentai/
│       ├── __init__.py
│       ├── indexer.py  # Document loading, chunking, filtering, index build/load
│       └── retriever.py # Clean retrieval interface over LlamaIndex
└── tests/
    ├── test_sanity.py   # Basic retrieval sanity checks
    └── test_retrieval.py # Transitive retrieval tests (A → B cases)
```

## Installation

Requires Python 3.10+. From the project root, with your virtual environment active:

```bash
pip install -e ".[test]"
```

## Running tests

```bash
pytest tests/ -v
```

The first run will download the embedding model (~130MB) and build the vector index from the RST source files. Subsequent runs load the index from disk and are fast.

## Documentation scope

Only human-authored RST files are indexed. The following are explicitly excluded:

- Auto-generated API reference files
- Sphinx templates and build artefacts
- Changelog
- `*_contents.rst` toctree wrappers
- Contribution guides and execution timing files

This keeps the index focused on content that is useful for answering user queries.

## Tests

### Sanity tests (`test_sanity.py`)

Basic checks that the retrieval pipeline is functioning correctly:

- The retriever returns results
- The correct number of results is returned
- Obvious queries return the expected source files (e.g. a launch query returns `launching_ansys_fluent.rst`)

### Transitive retrieval tests (`test_retrieval.py`)

These tests address a known limitation of classical vector similarity search: a query may clearly reference section **A**, but section **A** implicitly depends on section **B** — and the query contains nothing that directly points to **B**. A naive retriever returns `{A}` only; a good retriever returns `{A, B}`.

Each test case is defined as:

```python
{
    "query": "...",
    "expected_files": ["section_a.rst", "section_b.rst"],
    "notes": "Why B is implicitly required"
}
```

Retrieval is scored by **recall** over the expected set — did the retriever surface all expected sections, not just the most obvious one?

These tests are the primary benchmark for evaluating and comparing retrieval strategies.

## Retrieval scoring

Each test case is evaluated using recall:

```
recall = |retrieved ∩ expected| / |expected|
```

A recall of 1.0 means all expected sections were retrieved. The transitive `{A, B}` cases are specifically designed to expose the gap between classical vector search and more sophisticated retrieval strategies.