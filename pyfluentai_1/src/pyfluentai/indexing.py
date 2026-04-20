"""Shared indexing utilities used by both document and section indexers.

The helpers in this module define the common retrieval pipeline:
1) load source files,
2) split content into embedding chunks,
3) keep either information-rich chunks or short "stub" files,
4) build or load a vector index.

For AI practitioners, this is where recall and precision tradeoffs are tuned.
For example, MIN_CHARS controls noise filtering, while STUB_FILE_MAX_CHARS keeps
small but potentially important files available to retrieval.
"""

import os

from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

EMBED_MODEL_NAME = "BAAI/bge-small-en-v1.5"
MIN_CHARS = 300
STUB_FILE_MAX_CHARS = 1000

REQUIRED_EXTS = [".rst"]
EXCLUDE_FILES = [
    "changelog.rst",
    "contributing_contents.rst",
    "sg_execution_times.rst",
    "index.rst",
    "*_contents.rst",
]


def _configure_embedding():
    """Configure the global embedding model used by llama-index.

    The selected model maps text chunks into vector space so semantic retrieval
    can find conceptually related passages, not only keyword matches.
    """
    Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)


def _load_documents(doc_dir):
    """Load supported documentation files from disk.

    Parameters
    ----------
    doc_dir : str or path-like
        Root directory containing documentation sources.

    Returns
    -------
    list[Document]
        Llama-index document objects ready for chunking and indexing.
    """
    return SimpleDirectoryReader(
        input_dir=doc_dir,
        recursive=True,
        required_exts=REQUIRED_EXTS,
        exclude=EXCLUDE_FILES,
    ).load_data()


def _build_indexed_nodes(source_documents, file_name_key_name):
    """Split documents into retrieval nodes and filter low-signal content.

    Parameters
    ----------
    source_documents : list[Document]
        Input documents to split into embedding chunks.
    file_name_key_name : str
        Metadata field that stores the source file identifier for each node,
        for example "file_name" or "source_file".

    Returns
    -------
    list[BaseNode]
        Filtered chunk nodes suitable for vector indexing.

    Notes
    -----
    The filter keeps nodes that are long enough to carry signal, plus all nodes
    from short files ("stub files") so concise reference files are not dropped.
    """
    splitter = SentenceSplitter()
    nodes = splitter.get_nodes_from_documents(source_documents)
    return nodes


def load_or_build_index(doc_dir, persist_dir, document_to_section, file_name_key_name):
    """Load a persisted vector index or build one from source documents.

    Parameters
    ----------
    doc_dir : str or path-like
        Root documentation directory.
    persist_dir : str or path-like or None
        Directory containing persisted index artifacts. If missing or None, a
        fresh index is built.
    document_to_section : callable
        Transformation applied before chunking. This enables strategies such as
        raw-document indexing or section-aware indexing.
    file_name_key_name : str
        Metadata key used to identify source files during stub-file filtering.

    Returns
    -------
    VectorStoreIndex
        A vector index that can be queried through retrievers.
    """
    _configure_embedding()
    if persist_dir and os.path.exists(persist_dir):
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        return load_index_from_storage(storage_context)
    else:
        documents = _load_documents(doc_dir)
        nodes = _build_indexed_nodes(
            document_to_section(documents), file_name_key_name=file_name_key_name
        )
        index = VectorStoreIndex(nodes)
        if persist_dir:
            index.storage_context.persist(persist_dir=persist_dir)
        return index
