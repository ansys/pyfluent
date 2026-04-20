"""Top-level public API for pyfluentai.

The package exposes a practical default workflow for retrieval tasks:
- build an index using DocumentIndexer or SectionIndexer,
- query it through PyFluentRetriever.

Advanced section-labeling helpers are also exported for users building
graph-aware or metadata-rich retrieval pipelines.
"""

from pyfluentai._constants import FETCH_K
from pyfluentai.document_indexer import DocumentIndexer
from pyfluentai.labeling import (
    RelationEdge,
    SectionRecord,
    build_relation_edges,
    build_section_documents,
    build_section_documents_with_records_and_edges,
    export_label_artifacts,
    parse_rst_sections,
)
from pyfluentai.reranker import (
    CrossEncoderReranker,
    MergingReranker,
    NoOpReranker,
    Reranker,
)
from pyfluentai.retriever import PyFluentRetriever
from pyfluentai.section_indexer import SectionIndexer

__all__ = [
    "FETCH_K",
    "DocumentIndexer",
    "SectionIndexer",
    "PyFluentRetriever",
    "Reranker",
    "NoOpReranker",
    "CrossEncoderReranker",
    "MergingReranker",
    "RelationEdge",
    "SectionRecord",
    "build_relation_edges",
    "build_section_documents",
    "build_section_documents_with_records_and_edges",
    "export_label_artifacts",
    "parse_rst_sections",
]
