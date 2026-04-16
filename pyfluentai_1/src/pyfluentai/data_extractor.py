from collections import OrderedDict
from pathlib import Path
from typing import Any

from pyfluentai._constants import FETCH_K
from pyfluentai.prompt_generator import build_llm_messages
from pyfluentai.reranker import CrossEncoderRerankerWithMetadataBoost, NoOpReranker, Reranker
from pyfluentai.retriever import PyFluentRetriever
from pyfluentai.section_indexer import SectionIndexer

# ---------------------------------------------------------------------------
# Default Paths and Constants
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.parent.parent
DOC_DIR = ROOT / "docsource"
PERSIST_DIR = ROOT / "pyfluent_index" / "SectionIndexer"


class DataExtractor:
    """Extract query results into a compact ordered dictionary payload."""


    def __init__(
        self,
        re_ranker: Reranker = NoOpReranker(),
    ):
        index = SectionIndexer(
            doc_dir=str(DOC_DIR),
            persist_dir=str(PERSIST_DIR),
        ).get_index()
        self._retriever = PyFluentRetriever(
            index,
            top_k=FETCH_K,
        )
        self._re_ranker = re_ranker

    @staticmethod
    def _format_location(metadata: dict[str, Any]) -> str:
        source = metadata.get("source_file") or metadata.get("file_name") or "?"
        section = metadata.get("section_title", "")
        location = source if not section else f"{source} > {section}"
        return location

    @staticmethod
    def _format_text_with_lines(node_with_score: Any) -> str:
        text = node_with_score.text or ""
        text_lines = text.splitlines() or [""]
        return "\n".join(text_lines)

    @staticmethod
    def _build_payload(results: list[Any]) -> OrderedDict[str, dict[str, Any]]:
        payload: OrderedDict[str, dict[str, Any]] = OrderedDict()

        for index, item in enumerate(results, start=1):
            payload[f"data-{index}"] = {
                "normalized-score": round(float(item.score or 0.0), 4),
                "text": DataExtractor._format_text_with_lines(item),
                "location": DataExtractor._format_location(item.metadata or {}),
            }

        return payload

    def _extract(self, query: str) -> OrderedDict[str, dict[str, Any]]:
        baseline = self._retriever.retrieve(query)
        reranked = self._re_ranker.rerank(query, baseline)
        return self._build_payload(reranked)
    
    def extract(self, query: str) -> list[dict[str, str]]:
        return build_llm_messages(
            user_query=query,
            ordered_results=self._extract(query),
        )
    
    def update_re_ranker(self, re_ranker: Reranker) -> None:
        """Update the reranker used for post-retrieval processing."""
        self._re_ranker = re_ranker


if __name__ == "__main__":
    extractor = DataExtractor(re_ranker=CrossEncoderRerankerWithMetadataBoost(top_n=5))
    results = extractor.extract("How do I launch Fluent in a Slurm environment?")
    print(results)
