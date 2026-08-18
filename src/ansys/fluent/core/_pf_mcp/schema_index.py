# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Loads and indexes the Fluent settings schema JSON into a flat in-memory index.

The schema is the serialized output of ``get_static_info()`` from the Fluent
settings service.  Its root is a group node::

    {
        "type": "group",
        "children": {"setup": {...}, "solution": {...}, ...},
        "commands": {},
        "queries": {},
        "help": "..."
    }

Each node can be one of:
  - group       : has children / commands / queries
  - named-object: has object_type (instance template) + children + commands + queries
  - list-object : same as named-object but ordered
  - command     : has arguments dict
  - query       : has arguments dict + return_type
  - parameter   : integer / real / string / boolean / real-list / …

This module builds two flat dicts keyed by dot-path:
  _index        : path → SchemaNode
  _keyword_index: token  → [path, ...]

Named-object instance templates are indexed under ``<path>[*]``, so schema
validation works for both canonical paths like ``setup.materials.fluid[*].density``
and user-written paths like ``setup.materials.fluid["air"].density`` (after
:func:`canonicalize` normalises the bracket notation).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
import json
import pathlib
import re
from typing import Optional

SCHEMA_PATH = pathlib.Path(__file__).parent / "fluent_settings_schema.json"

# Matches instance brackets: ["air"], ['air'], [0], [42]
_INSTANCE_BRACKET_RE = re.compile(r'\[(?:"[^"]*"|\'[^\']*\'|\d+)\]')
_WORD_SPLIT_RE = re.compile(r"[\W]+")

# Node types that support get_state / set_state
_STATEFUL_TYPES = frozenset(
    {
        "group",
        "named-object",
        "list-object",
        "integer",
        "real",
        "string",
        "string/symbol",
        "boolean",
        "real-list",
        "integer-list",
        "string-list",
        "boolean-list",
        "vector",
        "material-property",
        "thread-var",
        "map",
        "file",
        "file-list",
    }
)


@dataclass
class SchemaNode:
    """Metadata for one node in the Fluent settings tree."""

    path: str
    type: str
    help: str = ""
    children_names: list[str] = field(default_factory=list)
    command_names: list[str] = field(default_factory=list)
    query_names: list[str] = field(default_factory=list)
    arguments: dict[str, dict] = field(default_factory=dict)
    api_exposure_level: str = ""
    return_type: str = ""

    @property
    def valid_ops(self) -> list[str]:
        """Return the operations that are valid for this node type."""
        if self.type == "command":
            return ["command"]
        if self.type == "query":
            return ["query"]
        if self.type in _STATEFUL_TYPES:
            return ["get_state", "set_state"]
        return ["get_state", "set_state"]

    def to_dict(self) -> dict:
        d: dict = {
            "path": self.path,
            "type": self.type,
            "help": self.help,
            "api_exposure_level": self.api_exposure_level,
            "valid_ops": self.valid_ops,
        }
        if self.children_names:
            d["children"] = self.children_names
        if self.command_names:
            d["commands"] = self.command_names
        if self.query_names:
            d["queries"] = self.query_names
        if self.arguments:
            d["arguments"] = self.arguments
        if self.return_type:
            d["return_type"] = self.return_type
        return d


_index: Optional[dict[str, SchemaNode]] = None
_keyword_index: Optional[dict[str, list[str]]] = None


def _join(parent: str, name: str) -> str:
    return f"{parent}.{name}" if parent else name


def _walk(
    node: dict,
    path: str,
    index: dict[str, SchemaNode],
    kw: dict[str, list[str]],
) -> None:
    node_type: str = node.get("type", "group")
    help_text: str = node.get("help", "")
    children: dict = node.get("children") or {}
    commands: dict = node.get("commands") or {}
    queries: dict = node.get("queries") or {}
    arguments: dict = node.get("arguments") or {}

    schema_node = SchemaNode(
        path=path,
        type=node_type,
        help=help_text,
        children_names=list(children.keys()),
        command_names=list(commands.keys()),
        query_names=list(queries.keys()),
        arguments={
            k: {"type": v.get("type", ""), "help": v.get("help", "")}
            for k, v in arguments.items()
        },
        api_exposure_level=node.get("api_exposure_level", ""),
        return_type=node.get("return_type", ""),
    )
    index[path] = schema_node

    # Keyword index: path segments + meaningful words from help text
    tokens: set[str] = set()
    for seg in re.split(r"[.\[\]*]+", path):
        if seg:
            tokens.add(seg.lower())
    for word in _WORD_SPLIT_RE.split(help_text.lower()):
        if len(word) > 2:
            tokens.add(word)
    for tok in tokens:
        kw[tok].append(path)

    # Recurse into sub-trees
    for name, child in children.items():
        if isinstance(child, dict):
            _walk(child, _join(path, name), index, kw)
    for name, child in commands.items():
        if isinstance(child, dict):
            _walk(child, _join(path, name), index, kw)
    for name, child in queries.items():
        if isinstance(child, dict):
            _walk(child, _join(path, name), index, kw)

    # Index named-object / list-object instance template under path[*]
    if node_type in ("named-object", "list-object"):
        obj_type = node.get("object_type")
        if obj_type and isinstance(obj_type, dict):
            _walk(obj_type, f"{path}[*]", index, kw)


def _load() -> tuple[dict[str, SchemaNode], dict[str, list[str]]]:
    global _index, _keyword_index
    if _index is not None:
        return _index, _keyword_index

    with open(SCHEMA_PATH, encoding="utf-8") as f:
        root = json.load(f)

    # Guard: if the root is a single-key wrapper dict (not a node itself), unwrap it
    if isinstance(root, dict) and "type" not in root and len(root) == 1:
        root = next(iter(root.values()))

    idx: dict[str, SchemaNode] = {}
    kw_raw: dict[str, list[str]] = defaultdict(list)
    _walk(root, "", idx, kw_raw)

    _index = idx
    _keyword_index = dict(kw_raw)
    return _index, _keyword_index


def get_index() -> dict[str, SchemaNode]:
    """Return the flat path→SchemaNode index (loaded lazily)."""
    return _load()[0]


def get_keyword_index() -> dict[str, list[str]]:
    """Return the token→[path] keyword index (loaded lazily)."""
    return _load()[1]


def canonicalize(path: str) -> str:
    """Normalise instance brackets to ``[*]`` for schema lookup.

    Examples::

        canonicalize('setup.materials.fluid["air"].density')
        # → 'setup.materials.fluid[*].density'

        canonicalize('setup.materials.fluid[0].density')
        # → 'setup.materials.fluid[*].density'
    """
    return _INSTANCE_BRACKET_RE.sub("[*]", path)
