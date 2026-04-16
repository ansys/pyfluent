"""Abstract and concrete reranker strategies for retrieval results."""

from __future__ import annotations
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from abc import ABC, abstractmethod
from typing import Any

# Fast, well-tested cross-encoder for passage reranking.  Runs locally via
# sentence-transformers with no API key required.
_DEFAULT_RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Keyword hints used to infer what content_type the query is targeting.
_CONTENT_TYPE_HINTS: dict[str, set[str]] = {
    "api_reference": {
        "api", "func", "function", "class", "method", "module",
        "returns", "parameter", "argument", "signature",
    },
    "user_guide": {
        "how", "guide", "tutorial", "setup", "configure",
        "workflow", "step", "use", "using", "enable",
    },
    "getting_started": {
        "install", "launch", "start", "begin", "quickstart",
        "introduction", "first",
    },
}


class Reranker(ABC):
    """Abstract interface for reranking retrieved candidates."""

    @abstractmethod
    def rerank(self, query: str, candidates: list[Any]) -> list[Any]:
        """Return candidates sorted by relevance (highest first)."""

    def _normalize_scores(self, items: list[Any]) -> list[Any]:
        """Normalize scores to 0-1 range based on min/max of all items.

        Parameters
        ----------
        items : list[Any]
            Items with scores to normalize.

        Returns
        -------
        list[Any]
            Items with normalized scores guaranteed to be in [0, 1] range.
        """
        if not items:
            return items

        scores = [float(item.score or 0.0) for item in items]
        min_score = min(scores)
        max_score = max(scores)

        if min_score == max_score:
            # All scores are equal; assign uniform middle value
            for item in items:
                item.score = 0.5
        else:
            # Normalize to 0-1 range
            for item in items:
                normalized = (float(item.score or 0.0) - min_score) / (max_score - min_score)
                # Ensure score is exactly in [0, 1] (handles floating point precision)
                item.score = max(0.0, min(1.0, normalized))

        return items


class NoOpReranker(Reranker):
    """Reranker that preserves incoming ranking."""

    def rerank(self, query: str, candidates: list[Any]) -> list[Any]:
        del query
        return self._normalize_scores(candidates)


class CrossEncoderReranker(Reranker):
    """Cross-encoder reranker using sentence-transformers via llama-index."""

    def __init__(self, model_name: str = _DEFAULT_RERANK_MODEL, top_n: int = 5):
        from llama_index.core.postprocessor import SentenceTransformerRerank
        self._cross_encoder = SentenceTransformerRerank(model=model_name or _DEFAULT_RERANK_MODEL, top_n=top_n)

    def rerank(self, query: str, candidates: list[Any]) -> list[Any]:
        from llama_index.core.schema import QueryBundle
        reranked = self._cross_encoder.postprocess_nodes(
            candidates, query_bundle=QueryBundle(query_str=query)
        )
        # Normalize scores based on all fetched candidates
        return self._normalize_scores(reranked)

class CrossEncoderRerankerWithMetadataBoost(Reranker):
    """Cross-encoder reranker with metadata-based score boosting."""

    def __init__(self, model_name: str = _DEFAULT_RERANK_MODEL, top_n: int = 5, boost_factor: float = 0.1):
        self._boost_factor = boost_factor
        self._cross_encoder = CrossEncoderReranker(model_name=model_name, top_n=top_n)

    def rerank(self, query: str, candidates: list[Any]) -> list[Any]:
        reranked = self._cross_encoder.rerank(query, candidates)
        query_tokens = self._tokenize_query(query)
        content_type_hint = self._infer_content_type_hint(query_tokens)
        rescored = [
            (
                float(item.score or 0.0)
                + self._boost_factor * self._metadata_bonus(item.node, content_type_hint),
                item,
            )
            for item in reranked
        ]
        rescored.sort(key=lambda x: x[0], reverse=True)
        
        # Update item scores to boosted scores, then normalize to [0, 1]
        for score, item in rescored:
            item.score = score
        
        reranked = [item for _, item in rescored]
        # Normalize scores based on all fetched candidates to ensure [0, 1] range
        reranked = self._normalize_scores(reranked)

        return reranked
    
    def _tokenize_query(self, query: str) -> set[str]:
        return {
            t.lower()
            for t in re.findall(r"[A-Za-z0-9_./:-]+", query)
            if len(t) >= 3
        }


    def _infer_content_type_hint(self, query_tokens: set[str]) -> str | None:
        """Return the most likely content_type for this query, or None."""
        best, best_score = None, 0
        for ctype, keywords in _CONTENT_TYPE_HINTS.items():
            score = len(query_tokens & keywords)
            if score > best_score:
                best_score, best = score, ctype
        return best if best_score > 0 else None

    def _metadata_bonus(
        self,
        node,
        content_type_hint: str | None,
    ) -> float:
        meta = getattr(node, "metadata", {}) or {}
        bonus = 0.0

        if content_type_hint and meta.get("content_type") == content_type_hint:
            bonus += 0.03

        bonus += 0.008 * min(float(meta.get("explicit_ref_count", 0)), 15)
        bonus += 0.005 * min(float(meta.get("anchor_count", 0)), 5)
        bonus += 0.005 * min(float(meta.get("toctree_entry_count", 0)), 5)

        return bonus


class MergingReranker(Reranker):
    """Composite reranker that runs multiple rerankers in parallel and merges scores.

    Each child reranker scores the same candidate set independently. Final scores
    are the average of each reranker's score for a given node, and results are
    returned sorted highest-first.

    Parameters
    ----------
    rerankers : list[Reranker]
        Two or more reranker instances to run in parallel.
    """

    def __init__(self, rerankers: list[Reranker]):
        if not rerankers:
            raise ValueError("MergingReranker requires at least one reranker.")
        self._rerankers = rerankers

    def rerank(self, query: str, candidates: list[Any]) -> list[Any]:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(r.rerank, query, candidates) for r in self._rerankers]
            all_results = [f.result() for f in as_completed(futures)]

        # Accumulate scores per node across all rerankers. Candidates omitted by
        # a child reranker are treated as contributing a default score of 0.0 so
        # the final average is over the full candidate set for every reranker.
        scores: dict[str, float] = {}
        nodes: dict[str, Any] = {item.node.node_id: item for item in candidates}
        reranker_count = len(self._rerankers)

        for results in all_results:
            for item in results:
                node_id = item.node.node_id
                scores[node_id] = scores.get(node_id, 0.0) + float(item.score or 0.0)
                nodes[node_id] = item

        # Average scores across every child reranker
        for item in nodes.values():
            nid = item.node.node_id
            item.score = scores.get(nid, 0.0) / reranker_count

        result_list = sorted(nodes.values(), key=lambda item: item.score, reverse=True)
        # Normalize scores based on all fetched candidates
        return self._normalize_scores(result_list)
