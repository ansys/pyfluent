"""Reranking demo for PyFluentRetriever.

Demonstrates the three retrieval strategies side-by-side:
  1. baseline   – top-5 from pure bi-encoder cosine similarity (no reranking)
  2. cross       – top-50 recall → cross-encoder reranking → top-5
  3. cross+meta  – same as above, with an additional metadata-signal boost

Run from the repo root:
    python examples/rerank_demo.py

The SectionIndexer index is reused from pyfluent_index/SectionIndexer if it
already exists, so the demo starts quickly on repeated runs.
"""

from pathlib import Path

from pyfluentai.reranker import (
    CrossEncoderReranker,
    CrossEncoderRerankerWithMetadataBoost,
    MergingReranker,
    NoOpReranker,
)
from pyfluentai.retriever import PyFluentRetriever
from pyfluentai.section_indexer import SectionIndexer

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.parent
DOC_DIR = ROOT / "docsource"
PERSIST_DIR = ROOT / "pyfluent_index" / "SectionIndexer"

# ---------------------------------------------------------------------------
# Queries to demonstrate
# ---------------------------------------------------------------------------
QUERIES = [
    "How do I launch Fluent with a specific number of processors?",
    # "How do I set boundary conditions in PyFluent?",
    # "How do I work with physical units?",
    # "How do I set up a meshing workflow?",
]

TOP_K = 5


def _print_results(label: str, results, query: str) -> None:
    print(f"\n{'='*70}")
    print(f"  Strategy : {label}")
    print(f"  Query    : {query}")
    print(f"{'='*70}")
    for rank, node in enumerate(results, start=1):
        meta = node.metadata or {}
        source = meta.get("source_file") or meta.get("file_name") or "?"
        section = meta.get("section_title", "")
        content_type = meta.get("content_type", "")
        score = f"{node.score:.4f}" if node.score is not None else "  n/a"
        explicit_refs = meta.get("explicit_ref_count", 0)
        anchors = meta.get("anchor_count", 0)
        print(
            f"  {rank}. [{score}] {source}"
            f"{' > ' + section if section else ''}"
            f"  ({content_type}, refs={explicit_refs}, anchors={anchors})"
        )
        snippet = node.text[:120].replace("\n", " ").strip()
        print(f'       "{snippet}..."')
    print()


def main():
    # Configure embedding model (must match what was used to build the index).
    # Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    print(f"\nLoading / building SectionIndexer from: {PERSIST_DIR}")
    index = SectionIndexer(
        doc_dir=str(DOC_DIR),
        persist_dir=str(PERSIST_DIR),
    ).get_index()
    print("Index ready.\n")

    # Build the two PyFluentRetriever variants once (cross-encoder loads once).
    retriever = PyFluentRetriever(
        index,
        top_k=TOP_K,
    )

    for query in QUERIES:
        # 1. Baseline: plain cosine similarity, no reranking.
        baseline = retriever.retrieve(query)
        reranker = NoOpReranker()
        no_op = reranker.rerank(
            query, baseline
        )  # Keep the baseline on the same reranker API path as the other strategies.
        _print_results("1 · Baseline  (bi-encoder cosine, top-5)", no_op, query)

        # 2. Cross-encoder: 50-candidate recall + cross-encoder reranking.
        reranker = CrossEncoderReranker(top_n=5)
        cross = reranker.rerank(query, baseline)
        _print_results(
            "2 · Cross-encoder  (recall-50 → MiniLM-L-6-v2 → top-5)",
            cross,
            query,
        )

        # 3. Cross-encoder + metadata signals.
        reranker = CrossEncoderRerankerWithMetadataBoost(top_n=5)
        cross_meta = reranker.rerank(query, baseline)
        _print_results(
            "3 · Cross-encoder + metadata boost  (content-type + ref/anchor signals)",
            cross_meta,
            query,
        )

        reranker = MergingReranker(
            [
                CrossEncoderReranker(top_n=2),
                CrossEncoderRerankerWithMetadataBoost(top_n=5),
            ]
        )
        merging = reranker.rerank(query, baseline)
        _print_results(
            "4 · Merging reranker  (average of cross-encoder and metadata boost)",
            merging,
            query,
        )


if __name__ == "__main__":
    main()
