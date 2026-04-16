"""Document-level indexer.

This indexer preserves the original document granularity before chunking. It is
useful when users want retrieval behavior that closely reflects source files,
rather than semantically labeled sections.
"""

from pyfluentai.indexing import load_or_build_index


class DocumentIndexer:
    """Build or load a vector index from raw documents.

    Parameters
    ----------
    doc_dir : str or path-like
        Root directory containing documentation inputs.
    persist_dir : str or path-like or None, optional
        Location for persisted index artifacts. If None, indexing happens fully
        in-memory for the current run.
    """

    def __init__(self, doc_dir, persist_dir=None):
        """Initialize document indexer configuration."""
        self.doc_dir = doc_dir
        self.persist_dir = persist_dir

    def get_index(self):
        """Return a vector index using document-level preprocessing.

        Returns
        -------
        VectorStoreIndex
            Index ready for semantic retrieval.
        """
        return load_or_build_index(
            self.doc_dir,
            self.persist_dir,
            lambda docs: docs,  # identity function since no sectioning
            file_name_key_name='file_name'
        )