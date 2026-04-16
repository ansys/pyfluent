
"""Retrieval wrapper for semantic search over pyfluentai indexes."""

from typing import Any

from pyfluentai._constants import FETCH_K


class PyFluentRetriever:
    """Retriever that performs similarity-based recall over a vector index.

    Parameters
    ----------
    index : VectorStoreIndex
        Pre-built vector index to query.
    top_k : int, optional
        Number of similarity-based results to return from the underlying
        retriever.
    """

    def __init__(
        self,
        index,
        top_k: int = FETCH_K,
    ):
        self._retriever = index.as_retriever(similarity_top_k=top_k)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def retrieve(self, query: str) -> list[Any]:
        """Return the top-k most relevant nodes for the query.

        Parameters
        ----------
        query : str
            User question or search phrase.
        Returns
        -------
        list[NodeWithScore]
            Retrieval results returned directly by the underlying vector
            retriever.
        """
        return self._retriever.retrieve(query)
