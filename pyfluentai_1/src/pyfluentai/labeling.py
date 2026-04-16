"""Section labeling and relation extraction for documentation-aware AI retrieval.

This module converts reStructuredText documents into structured section records
and typed relation edges. The output supports several AI workflows:

- retrieval with richer metadata than plain chunks,
- graph-augmented reranking and navigation,
- analysis of documentation coverage and cross-link quality.

The design favors deterministic parsing and stable identifiers so outputs remain
comparable across runs and can be versioned reliably.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
from typing import Any

from llama_index.core.schema import Document


HEADING_LEVELS = {
    "=": 1,
    "-": 2,
    "~": 3,
    "^": 4,
    '"': 5,
}

LABEL_RE = re.compile(r"^\.\. _([^:]+):\s*$", re.MULTILINE)
DIRECTIVE_RE = re.compile(r"^\.\. ([a-zA-Z0-9_-]+)::")
ROLE_PATTERNS = {
    "ref": re.compile(r":ref:`([^`]+)`"),
    "doc": re.compile(r":doc:`([^`]+)`"),
    "obj": re.compile(r":obj:`([^`]+)`"),
    "py:func": re.compile(r":py:func:`([^`]+)`"),
    "py:class": re.compile(r":py:class:`([^`]+)`"),
    "py:meth": re.compile(r":py:meth:`([^`]+)`"),
    "py:mod": re.compile(r":py:mod:`([^`]+)`"),
}


@dataclass(frozen=True)
class RelationEdge:
    """Typed edge connecting a section record to another entity.

    Edges encode semantics such as explicit references, defined anchors, and
    toctree containment. This structure is useful for knowledge-graph style
    retrieval or explainability of why a chunk was retrieved.
    """

    edge_id: str
    source_id: str
    target_id: str
    relation_type: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the edge as a plain dictionary."""
        return asdict(self)


@dataclass(frozen=True)
class SectionRecord:
    """Structured representation of one parsed documentation section.

    A section record preserves source boundaries, heading hierarchy, and
    reference metadata. It can be used directly for indexing or exported as a
    training/evaluation artifact for downstream AI tasks.
    """

    record_id: str
    source_file: str
    section_title: str
    heading_level: int
    heading_path: list[str]
    line_start: int
    line_end: int
    anchor_ids: list[str]
    explicit_refs: list[dict[str, str]]
    directives: list[str]
    toctree_entries: list[str]
    content_type: str
    text: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the section record as a plain dictionary."""
        return asdict(self)


def slugify_heading(value: str) -> str:
    """Convert a heading into a stable slug fragment."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "section"


def stable_record_id(source_file: str, heading_path: list[str], line_start: int) -> str:
    """Build a deterministic section identifier.

    Deterministic IDs make it easier to diff graph artifacts between commits and
    to cache downstream computations.
    """
    if heading_path:
        suffix = "/".join(slugify_heading(part) for part in heading_path)
    else:
        suffix = f"preamble-{line_start}"
    return f"{source_file}::{suffix}"


def _normalize_source_file(metadata: dict[str, Any]) -> str:
    """Normalize source-file metadata to repository-relative POSIX style."""
    raw_path = metadata.get("file_path") or metadata.get("file_name") or "unknown"
    normalized = str(raw_path).replace("\\", "/")
    marker = "/docsource/"
    if marker in normalized:
        normalized = normalized.split(marker, 1)[1]
    return PurePosixPath(normalized).as_posix()


def _content_type_for(source_file: str) -> str:
    """Infer a coarse content type from the documentation path."""
    if source_file.startswith("api/"):
        return "api_reference"
    if source_file.startswith("user_guide/"):
        return "user_guide"
    if source_file.startswith("getting_started/"):
        return "getting_started"
    if source_file.startswith("contributing/"):
        return "contributing"
    return "documentation"


def _is_heading_underline(line: str) -> bool:
    """Return True when a line matches an RST heading underline marker."""
    stripped = line.strip()
    return bool(stripped) and len(set(stripped)) == 1 and stripped[0] in HEADING_LEVELS


def _find_heading_rows(lines: list[str]) -> list[tuple[int, str, int]]:
    """Locate RST heading rows as (line_index, title, heading_level)."""
    headings: list[tuple[int, str, int]] = []
    for index in range(len(lines) - 1):
        title = lines[index].rstrip()
        underline = lines[index + 1].rstrip()
        if not title.strip() or not _is_heading_underline(underline):
            continue
        if len(underline.strip()) < len(title.strip()):
            continue
        headings.append((index, title.strip(), HEADING_LEVELS[underline.strip()[0]]))
    return headings


def _expand_heading_start(lines: list[str], heading_index: int, lower_bound: int) -> int:
    """Expand section start upward to include labels adjacent to a heading."""
    cursor = heading_index
    while cursor - 1 >= lower_bound:
        candidate = lines[cursor - 1].rstrip()
        if not candidate:
            cursor -= 1
            continue
        if LABEL_RE.fullmatch(candidate):
            cursor -= 1
            continue
        break
    return cursor


def _normalize_role_target(raw_target: str) -> str:
    """Normalize an interpreted-text role target.

    Handles forms like "label <target>" and strips role-specific decoration.
    """
    target = raw_target.strip()
    if "<" in target and target.endswith(">"):
        _, resolved = target.rsplit("<", 1)
        target = resolved[:-1].strip()
    return target.lstrip("~")


def _extract_explicit_refs(text: str) -> list[dict[str, str]]:
    """Extract supported interpreted-text role references from RST content."""
    refs: list[dict[str, str]] = []
    for role, pattern in ROLE_PATTERNS.items():
        for match in pattern.finditer(text):
            target = _normalize_role_target(match.group(1))
            refs.append({"role": role, "target": target})
    return refs


def _extract_directives(text: str) -> list[str]:
    """Extract directive names present in a section body."""
    directives: list[str] = []
    for line in text.splitlines():
        match = DIRECTIVE_RE.match(line.strip())
        if match:
            directives.append(match.group(1))
    return sorted(set(directives))


def _extract_toctree_entries(lines: list[str]) -> list[str]:
    """Extract entries from any toctree directives in the provided lines."""
    entries: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].strip() != ".. toctree::":
            index += 1
            continue

        index += 1
        while index < len(lines):
            line = lines[index]
            stripped = line.strip()
            if not stripped:
                index += 1
                continue
            if not line.startswith((" ", "\t")):
                break
            if stripped.startswith(":"):
                index += 1
                continue
            entries.append(stripped)
            index += 1
    return entries


def parse_rst_sections(text: str, source_file: str) -> list[SectionRecord]:
    """Parse an RST document into section records.

    Parameters
    ----------
    text : str
        Full text of one source document.
    source_file : str
        Normalized path used as provenance for generated records.

    Returns
    -------
    list[SectionRecord]
        Ordered section records covering preamble and heading-based sections.
    """
    lines = text.splitlines()
    headings = _find_heading_rows(lines)
    content_type = _content_type_for(source_file)

    if not headings:
        section_text = text.strip()
        if not section_text:
            return []
        record = SectionRecord(
            record_id=stable_record_id(source_file, [], 1),
            source_file=source_file,
            section_title=PurePosixPath(source_file).stem,
            heading_level=0,
            heading_path=[],
            line_start=1,
            line_end=len(lines),
            anchor_ids=LABEL_RE.findall(text),
            explicit_refs=_extract_explicit_refs(text),
            directives=_extract_directives(text),
            toctree_entries=_extract_toctree_entries(lines),
            content_type=content_type,
            text=section_text,
        )
        return [record]

    adjusted_starts: list[int] = []
    lower_bound = 0
    for heading_index, _, _ in headings:
        adjusted = _expand_heading_start(lines, heading_index, lower_bound)
        adjusted_starts.append(adjusted)
        lower_bound = adjusted + 1

    records: list[SectionRecord] = []
    heading_path: list[str] = []

    if adjusted_starts[0] > 0:
        preamble_lines = lines[:adjusted_starts[0]]
        preamble_text = "\n".join(preamble_lines).strip()
        if preamble_text:
            records.append(
                SectionRecord(
                    record_id=stable_record_id(source_file, [], 1),
                    source_file=source_file,
                    section_title=PurePosixPath(source_file).stem,
                    heading_level=0,
                    heading_path=[],
                    line_start=1,
                    line_end=adjusted_starts[0],
                    anchor_ids=LABEL_RE.findall(preamble_text),
                    explicit_refs=_extract_explicit_refs(preamble_text),
                    directives=_extract_directives(preamble_text),
                    toctree_entries=_extract_toctree_entries(preamble_lines),
                    content_type=content_type,
                    text=preamble_text,
                )
            )

    for idx, (_, title, level) in enumerate(headings):
        start = adjusted_starts[idx]
        end = adjusted_starts[idx + 1] if idx + 1 < len(adjusted_starts) else len(lines)
        section_lines = lines[start:end]
        section_text = "\n".join(section_lines).strip()
        if not section_text:
            continue

        if level <= len(heading_path):
            heading_path = heading_path[: level - 1]
        heading_path.append(title)

        records.append(
            SectionRecord(
                record_id=stable_record_id(source_file, heading_path, start + 1),
                source_file=source_file,
                section_title=title,
                heading_level=level,
                heading_path=list(heading_path),
                line_start=start + 1,
                line_end=end,
                anchor_ids=LABEL_RE.findall(section_text),
                explicit_refs=_extract_explicit_refs(section_text),
                directives=_extract_directives(section_text),
                toctree_entries=_extract_toctree_entries(section_lines),
                content_type=content_type,
                text=section_text,
            )
        )

    return records


def build_relation_edges(records: list[SectionRecord]) -> list[RelationEdge]:
    """Generate relation edges from parsed section records.

    The generated edges capture:
    - anchor definitions,
    - explicit references to docs/anchors/API entities,
    - toctree containment links.
    """
    edges: list[RelationEdge] = []
    for record in records:
        for anchor_id in record.anchor_ids:
            edge_key = f"{record.record_id}|defines|anchor:{anchor_id}"
            edges.append(
                RelationEdge(
                    edge_id=hashlib.sha1(edge_key.encode("utf-8")).hexdigest(),
                    source_id=record.record_id,
                    target_id=f"anchor:{anchor_id}",
                    relation_type="defines_anchor",
                    metadata={"source_file": record.source_file},
                )
            )
        for ref in record.explicit_refs:
            role = ref["role"]
            target = ref["target"]
            edge_key = f"{record.record_id}|{role}|{target}"
            prefix = "entity" if role.startswith("py:") or role == "obj" else "anchor"
            relation_type = "api_symbol_ref" if prefix == "entity" else "references"
            edges.append(
                RelationEdge(
                    edge_id=hashlib.sha1(edge_key.encode("utf-8")).hexdigest(),
                    source_id=record.record_id,
                    target_id=f"{prefix}:{target}",
                    relation_type=relation_type,
                    metadata={"role": role, "source_file": record.source_file},
                )
            )
        for target in record.toctree_entries:
            edge_key = f"{record.record_id}|toctree|{target}"
            edges.append(
                RelationEdge(
                    edge_id=hashlib.sha1(edge_key.encode("utf-8")).hexdigest(),
                    source_id=record.record_id,
                    target_id=f"doc:{target}",
                    relation_type="contains",
                    metadata={"source_file": record.source_file},
                )
            )
    return edges


def build_section_documents_with_records_and_edges(
    documents: list[Document],
) -> tuple[list[Document], list[SectionRecord], list[RelationEdge]]:
    """Transform source documents into section documents, records, and edges.

    This function is the bridge between deterministic parsing and embedding
    workflows: each section becomes a Document with compact metadata suitable for
    chunking and vector indexing. It also returns the richer structural artifacts
    produced during parsing.
    """
    section_documents: list[Document] = []
    records: list[SectionRecord] = []

    for document in documents:
        source_file = _normalize_source_file(document.metadata)
        section_records = parse_rst_sections(document.text, source_file)
        records.extend(section_records)
        for record in section_records:
            metadata = dict(document.metadata)
            metadata.update(
                {
                    "source_file": record.source_file,
                    "record_id": record.record_id,
                    "section_title": record.section_title,
                    "heading_level": record.heading_level,
                    "content_type": record.content_type,
                    "line_start": record.line_start,
                    "line_end": record.line_end,
                    # Keep metadata compact for embedding/chunking. Rich relation fields
                    # remain available via records/edges JSONL artifacts.
                    "anchor_count": len(record.anchor_ids),
                    "explicit_ref_count": len(record.explicit_refs),
                    "directive_count": len(record.directives),
                    "toctree_entry_count": len(record.toctree_entries),
                }
            )
            section_documents.append(Document(text=record.text, metadata=metadata))
    return section_documents, records, build_relation_edges(records)


def build_section_documents(documents: list[Document]) -> list[Document]:
    """Transform source documents into section documents for indexing.

    This is the simplified interface for callers that only need the document
    objects used by the indexing pipeline.
    """
    return build_section_documents_with_records_and_edges(documents)[0]


def export_label_artifacts(records: list[SectionRecord], edges: list[RelationEdge], output_dir: str) -> None:
    """Write section records and edges as JSONL artifacts.

    The exported files are intentionally line-oriented to make them easy to diff,
    stream, and post-process with common data tooling.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    records_path = output_path / "records.jsonl"
    edges_path = output_path / "edges.jsonl"

    with records_path.open("w", encoding="utf-8") as records_file:
        for record in records:
            records_file.write(json.dumps(record.to_dict(), sort_keys=True) + "\n")

    with edges_path.open("w", encoding="utf-8") as edges_file:
        for edge in edges:
            edges_file.write(json.dumps(edge.to_dict(), sort_keys=True) + "\n")