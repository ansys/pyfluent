"""Prompt generation utilities for user-facing answers from retrieval results."""

from __future__ import annotations

from collections import OrderedDict
import json
from typing import Any


def _serialize_ordered_results(
    ordered_results: OrderedDict[str, dict[str, Any]],
    max_items: int,
) -> str:
    """Serialize ordered retrieval results for prompt inclusion."""
    trimmed: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for index, (key, value) in enumerate(ordered_results.items()):
        if index >= max_items:
            break
        trimmed[key] = {
            "normalized-score": value.get("normalized-score", 0.0),
            "location": value.get("location", ""),
            "text": value.get("text", ""),
        }
    return json.dumps(trimmed, indent=2, ensure_ascii=True)


def build_system_prompt() -> str:
    """Return system instruction for grounded, user-facing response generation."""
    return (
        "You are a precise technical assistant for PyFluent documentation. "
        "Answer only from the provided context snippets. "
        "If context is insufficient, say so explicitly and ask one focused follow-up question. "
        "Do not fabricate APIs, arguments, or behavior. "
        "Prioritize higher normalized-score evidence first, while cross-checking consistency across snippets. "
        "When possible, give actionable steps, concise code examples, and caveats. "
        "Always include citations in the form [source: <location>] at the end of each major claim. "
        "If two snippets conflict, acknowledge uncertainty and present both with citations. "
        "Write in a clear user-facing style: summary first, then steps/details."
    )


def build_user_prompt(
    user_query: str,
    ordered_results: OrderedDict[str, dict[str, Any]],
    max_items: int = 8,
) -> str:
    """Build a complete user prompt using ordered retrieval results.

    Parameters
    ----------
    user_query : str
            The user question to answer.
    ordered_results : OrderedDict[str, dict[str, Any]]
            Retrieval payload from DataExtractor.extract() / extract_data().
    max_items : int, optional
            Maximum number of ranked entries to include in context.
    """
    serialized_context = _serialize_ordered_results(
        ordered_results, max_items=max_items
    )

    return (
        "Task: Answer the user query using ONLY the provided ranked context.\n\n"
        f"User Query:\n{user_query}\n\n"
        "Ranked Context (OrderedDictionary JSON):\n"
        f"{serialized_context}\n\n"
        "Required Output Structure:\n"
        "1) Direct Answer (2-5 sentences).\n"
        "2) Practical Steps (numbered, if applicable).\n"
        "3) Optional Example (short code or command, if supported by context).\n"
        "4) Notes/Caveats (only if needed).\n"
        "5) Sources Used (bullet list with exact location strings).\n\n"
        "Grounding Rules:\n"
        "- Use only information present in context text fields.\n"
        "- Prefer higher normalized-score entries when evidence overlaps.\n"
        "- Keep citations inline as [source: <location>].\n"
        "- Do not mention internal ranking mechanics unless asked.\n"
        "- If answer is not fully supported, state what is missing and ask one clarifying question."
    )


def build_llm_messages(
    user_query: str,
    ordered_results: OrderedDict[str, dict[str, Any]],
    max_items: int = 8,
) -> list[dict[str, str]]:
    """Return chat-completion style messages ready to send to an LLM."""
    return [
        {"role": "system", "content": build_system_prompt()},
        {
            "role": "user",
            "content": build_user_prompt(
                user_query=user_query,
                ordered_results=ordered_results,
                max_items=max_items,
            ),
        },
    ]
