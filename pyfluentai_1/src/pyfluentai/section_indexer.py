"""Section-aware indexer.

This indexer transforms documents into labeled sections before chunking. The
extra structure can improve retrieval grounding because each chunk carries
section context (title, heading level, content type, and source metadata).
"""

from pyfluentai.indexing import load_or_build_index
from pyfluentai.labeling import build_section_documents


class SectionIndexer:
    """Build or load a vector index from sectionized documents.

    Parameters
    ----------
    doc_dir : str or path-like
        Root directory containing documentation inputs.
    persist_dir : str or path-like or None, optional
        Location for persisted index artifacts. If None, indexing happens fully
        in-memory for the current run.
    """

    def __init__(self, doc_dir, persist_dir=None):
        """Initialize section indexer configuration."""
        self.doc_dir = doc_dir
        self.persist_dir = persist_dir

    def get_index(self):
        """Return a vector index using section-aware preprocessing.

        Returns
        -------
        VectorStoreIndex
            Index ready for semantic retrieval.
        """
        return load_or_build_index(
            self.doc_dir,
            self.persist_dir,
            lambda docs: build_section_documents(docs),
            file_name_key_name='source_file'
        )