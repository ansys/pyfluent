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

"""Pure-Python implementations of the five MCP tools.

These functions have no MCP protocol dependency so they can be unit-tested
against a synthetic schema without running the MCP server.

Workflow recommended for LLMs
------------------------------
1. ``fluent_search(keyword)``           – find candidate paths by keyword
2. ``fluent_browse(path)``              – explore children / commands / queries
3. ``fluent_info(path)``                – inspect types, arguments, valid ops
4. ``fluent_validate_path(path)``       – confirm the path is correct
5. ``fluent_generate_script(ops)``      – emit the final Python script
"""

from __future__ import annotations

import re
from typing import Any

from .schema_index import SchemaNode, canonicalize, get_index, get_keyword_index

_WORD_RE = re.compile(r"\b\w+\b")


# ---------------------------------------------------------------------------
# Tool 1 – browse
# ---------------------------------------------------------------------------


def fluent_browse(path: str = "") -> dict:
    """List children, commands, and queries available at *path*.

    Parameters
    ----------
    path:
        Dot-separated path into the settings tree.  Use ``""`` for the root.
        Named-object instance brackets are normalised automatically, e.g.
        ``'setup.materials.fluid["air"]'`` is treated as
        ``'setup.materials.fluid[*]'``.

    Returns
    -------
    dict
        ``{path, type, help, valid_ops, children?, commands?, queries?,
           instance_template?}``
    """
    idx = get_index()
    canonical = canonicalize(path)
    node: SchemaNode | None = idx.get(canonical)

    if node is None:
        # Try to give useful suggestions
        prefix = canonical + "." if canonical else ""
        suggestions = sorted([p for p in idx if p.startswith(prefix)][:8], key=len)
        if not suggestions and canonical:
            # parent-level suggestions
            parent = canonical.rsplit(".", 1)[0]
            suggestions = sorted([p for p in idx if p.startswith(parent)][:8], key=len)
        return {
            "error": f"Path '{path}' not found in schema.",
            "suggestions": suggestions,
        }

    result: dict[str, Any] = {
        "path": path,
        "type": node.type,
        "help": node.help,
        "valid_ops": node.valid_ops,
    }

    if node.children_names:
        result["children"] = _summarise_children(canonical, node.children_names, idx)

    if node.command_names:
        result["commands"] = _summarise_commands(canonical, node.command_names, idx)

    if node.query_names:
        result["queries"] = _summarise_queries(canonical, node.query_names, idx)

    if node.type in ("named-object", "list-object"):
        template_path = f"{canonical}[*]"
        tmpl: SchemaNode | None = idx.get(template_path)
        if tmpl:
            result["instance_template"] = {
                "access_pattern": f'{path}["<name>"]',
                "children": tmpl.children_names,
                "commands": tmpl.command_names,
                "queries": tmpl.query_names,
            }

    return result


def _child_path(parent: str, name: str) -> str:
    return f"{parent}.{name}" if parent else name


def _summarise_children(parent: str, names: list[str], idx: dict) -> list[dict]:
    out = []
    for name in names:
        child: SchemaNode | None = idx.get(_child_path(parent, name))
        out.append(
            {
                "name": name,
                "type": child.type if child else "unknown",
                "help": _truncate(child.help if child else "", 120),
            }
        )
    return out


def _summarise_commands(parent: str, names: list[str], idx: dict) -> list[dict]:
    out = []
    for name in names:
        cmd: SchemaNode | None = idx.get(_child_path(parent, name))
        out.append(
            {
                "name": name,
                "help": _truncate(cmd.help if cmd else "", 120),
                "arguments": cmd.arguments if cmd else {},
            }
        )
    return out


def _summarise_queries(parent: str, names: list[str], idx: dict) -> list[dict]:
    out = []
    for name in names:
        qry: SchemaNode | None = idx.get(_child_path(parent, name))
        out.append(
            {
                "name": name,
                "help": _truncate(qry.help if qry else "", 120),
                "arguments": qry.arguments if qry else {},
                "return_type": qry.return_type if qry else "",
            }
        )
    return out


# ---------------------------------------------------------------------------
# Tool 2 – info
# ---------------------------------------------------------------------------


def fluent_info(path: str) -> dict:
    """Return full schema metadata for *path*.

    Parameters
    ----------
    path:
        Exact dot-path, e.g. ``'setup.models.viscous.model'``.

    Returns
    -------
    dict
        All SchemaNode fields plus ``valid_ops``.  Returns ``{"error": ...}``
        if the path is not found.
    """
    idx = get_index()
    canonical = canonicalize(path)
    node: SchemaNode | None = idx.get(canonical)

    if node is None:
        return {
            "error": f"Path '{path}' (canonical: '{canonical}') not found in schema."
        }

    return node.to_dict()


# ---------------------------------------------------------------------------
# Tool 3 – search
# ---------------------------------------------------------------------------


def fluent_search(keyword: str, limit: int = 20) -> list[dict]:
    """Search for Fluent paths by keyword (path segments and help text).

    Parameters
    ----------
    keyword:
        One or more words, e.g. ``'viscous turbulence'``.
    limit:
        Maximum number of results.

    Returns
    -------
    list[dict]
        Ranked list of ``{path, type, help, valid_ops}``.
    """
    idx = get_index()
    kw_idx = get_keyword_index()
    kl = keyword.lower()

    scores: dict[str, float] = {}

    # Token hits (weighted higher)
    for token in _WORD_RE.findall(kl):
        for p in kw_idx.get(token, []):
            scores[p] = scores.get(p, 0.0) + 2.0

    # Substring fallback for paths and help not caught by token index
    for p, node in idx.items():
        if p not in scores:
            if kl in p.lower():
                scores[p] = 1.5
            elif kl in node.help.lower():
                scores[p] = 1.0

    # Sort: score desc, path length asc (prefer shallower nodes)
    ranked = sorted(scores, key=lambda p: (-scores[p], len(p)))[:limit]

    return [
        {
            "path": p,
            "type": idx[p].type,
            "help": _truncate(idx[p].help, 150),
            "valid_ops": idx[p].valid_ops,
        }
        for p in ranked
    ]


# ---------------------------------------------------------------------------
# Tool 4 – validate_path
# ---------------------------------------------------------------------------


def fluent_validate_path(path: str) -> dict:
    """Check whether *path* exists in the schema.

    Instance brackets (``["air"]``, ``[0]``) are normalised to ``[*]``
    before the lookup so user-written paths are validated correctly.

    Parameters
    ----------
    path:
        Path to validate.  May contain instance brackets.

    Returns
    -------
    dict
        ``{valid, canonical_path, input_path, node_type, valid_ops}`` on
        success or ``{valid: False, ..., error, suggestions}`` on failure.
    """
    idx = get_index()
    canonical = canonicalize(path)
    node: SchemaNode | None = idx.get(canonical)

    if node is not None:
        return {
            "valid": True,
            "input_path": path,
            "canonical_path": canonical,
            "node_type": node.type,
            "valid_ops": node.valid_ops,
        }

    # Build suggestions from sibling paths
    parent = canonical.rsplit(".", 1)[0] if "." in canonical else ""
    suggestions = sorted(
        [p for p in idx if p.startswith(parent + ".") or (not parent and "." not in p)][
            :8
        ],
        key=len,
    )

    return {
        "valid": False,
        "input_path": path,
        "canonical_path": canonical,
        "error": f"Path '{canonical}' not found in schema.",
        "suggestions": suggestions,
    }


# ---------------------------------------------------------------------------
# Tool 5 – generate_script
# ---------------------------------------------------------------------------


def fluent_generate_script(
    operations: list[dict],
    session_var: str = "solver",
    include_launch: bool = True,
) -> dict:
    """Generate a complete, runnable PyFluent Python script.

    Each element in *operations* must be a dict with:

    .. code-block:: text

        {
            "path"      : "setup.models.viscous.model",   # required
            "op"        : "set_state",                    # required
            "value"     : "k-omega-sst",                  # for set_state
            "args"      : {"type": "solid", "name": "x"}, # for command / query
            "result_var": "my_var",                       # optional capture name
            "comment"   : "Enable turbulence model"       # optional comment
        }

    Supported *op* values
    ~~~~~~~~~~~~~~~~~~~~~~
    ``get_state``  – ``result = <path>.get_state()``
    ``set_state``  – ``<path>.set_state(<value>)``
    ``command``    – ``<path>(**args)``
    ``query``      – ``result = <path>(**args)``

    Parameters
    ----------
    operations:
        Ordered list of operation dicts (see above).
    session_var:
        Python variable name for the Fluent session object (default ``solver``).
    include_launch:
        When ``True`` (default), wraps the operations with
        ``pyfluent.launch_fluent()`` and ``solver.exit()`` boilerplate.

    Returns
    -------
    dict
        ``{script: str, validation_errors: list}``
    """
    idx = get_index()
    errors: list[dict] = []
    code_lines: list[str] = []
    result_counter = [0]

    def _next_var() -> str:
        result_counter[0] += 1
        return f"result_{result_counter[0]}"

    for i, op in enumerate(operations):
        path: str = op.get("path", "")
        operation: str = op.get("op", "")

        # Basic presence checks
        if not path:
            errors.append({"index": i, "error": "Missing 'path'."})
            code_lines.append("# ERROR: operation missing 'path'")
            continue
        if not operation:
            errors.append({"index": i, "error": "Missing 'op'."})
            code_lines.append(f"# ERROR: operation on '{path}' missing 'op'")
            continue

        canonical = canonicalize(path)
        node: SchemaNode | None = idx.get(canonical)

        if node is None:
            errors.append(
                {
                    "index": i,
                    "path": path,
                    "error": f"Path '{canonical}' not found in schema.",
                }
            )
            code_lines.append(f"# ERROR: path not found in schema: {path}")
            continue

        # Optional inline comment
        if op.get("comment"):
            code_lines.append(f"# {op['comment']}")

        python_ref = _python_ref(path, session_var)
        result_var: str = op.get("result_var") or _next_var()

        if operation == "set_state":
            if node.type in ("command", "query"):
                errors.append(
                    {
                        "index": i,
                        "path": path,
                        "error": f"set_state is not valid on a '{node.type}' node.",
                    }
                )
                code_lines.append(f"# ERROR: cannot set_state on {node.type} '{path}'")
            else:
                value = op.get("value")
                code_lines.append(f"{python_ref}.set_state({_fmt(value)})")

        elif operation == "get_state":
            if node.type in ("command", "query"):
                errors.append(
                    {
                        "index": i,
                        "path": path,
                        "error": f"get_state is not valid on a '{node.type}' node.",
                    }
                )
                code_lines.append(f"# ERROR: cannot get_state on {node.type} '{path}'")
            else:
                code_lines.append(f"{result_var} = {python_ref}.get_state()")

        elif operation == "command":
            if node.type != "command":
                errors.append(
                    {
                        "index": i,
                        "path": path,
                        "error": f"'{path}' has type '{node.type}', expected 'command'.",
                    }
                )
                code_lines.append(f"# ERROR: not a command: {path} (type={node.type})")
            else:
                args = op.get("args") or {}
                code_lines.append(f"{python_ref}({_fmt_kwargs(args)})")

        elif operation == "query":
            if node.type != "query":
                errors.append(
                    {
                        "index": i,
                        "path": path,
                        "error": f"'{path}' has type '{node.type}', expected 'query'.",
                    }
                )
                code_lines.append(f"# ERROR: not a query: {path} (type={node.type})")
            else:
                args = op.get("args") or {}
                code_lines.append(f"{result_var} = {python_ref}({_fmt_kwargs(args)})")

        else:
            errors.append(
                {
                    "index": i,
                    "error": (
                        f"Unknown op '{operation}'. Valid values: "
                        "get_state, set_state, command, query."
                    ),
                }
            )
            code_lines.append(f"# ERROR: unknown op '{operation}'")

    # Assemble the full script
    parts: list[str] = []

    if include_launch:
        parts.append("import ansys.fluent.core as pyfluent\n")
        parts.append(f"\n{session_var} = pyfluent.launch_fluent(mode='solver')\n")

    if code_lines:
        parts.append("\n")
        for line in code_lines:
            parts.append(line + "\n")

    if include_launch:
        parts.append(f"\n{session_var}.exit()\n")

    return {
        "script": "".join(parts),
        "validation_errors": errors,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _python_ref(path: str, session_var: str) -> str:
    """Convert a settings path to a Python attribute-access expression."""
    if not path:
        return f"{session_var}.settings"
    return f"{session_var}.settings.{path}"


def _fmt(value: Any) -> str:
    """Format a value as a Python literal suitable for generated code."""
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, (int, float)):
        return str(value)
    # dict / list – repr produces valid Python
    return repr(value)


def _fmt_kwargs(args: dict) -> str:
    """Format a dict as a keyword-argument string."""
    if not args:
        return ""
    return ", ".join(f"{k}={_fmt(v)}" for k, v in args.items())


def _truncate(text: str, max_len: int) -> str:
    return text[:max_len] + "…" if len(text) > max_len else text
