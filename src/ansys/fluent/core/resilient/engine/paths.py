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

"""Resolve settings paths against a live settings tree.

Two path forms are supported:

* dotted Python paths such as ``setup.boundary_conditions["inlet"].momentum``
  (used by adapters, for example in activation candidates), and
* slash-separated server paths such as ``setup/boundary-conditions/inlet`` (used
  by the settings service, and therefore by intercepted writes).
"""

from __future__ import annotations

import re
from typing import Any

from .exceptions import PathResolutionError

#: A path segment with an optional ``["key"]`` / ``['key']`` / ``[index]`` suffix.
_SEGMENT_RE = re.compile(
    r"""(?P<name>[A-Za-z_][A-Za-z0-9_]*)
        (?:\[\s*(?P<key>"[^"]*"|'[^']*'|\d+)\s*\])?""",
    re.VERBOSE,
)


def _strip_quotes(key: str) -> str:
    key = key.strip()
    if len(key) >= 2 and key[0] in "\"'" and key[-1] == key[0]:
        return key[1:-1]
    return key


def _split_dotted(path: str) -> list[str]:
    """Split a dotted path on dots that are not inside ``[...]`` keys."""
    parts: list[str] = []
    depth = 0
    current: list[str] = []
    for char in path:
        if char == "[":
            depth += 1
        elif char == "]":
            depth = max(0, depth - 1)
        if char == "." and depth == 0:
            parts.append("".join(current))
            current = []
        else:
            current.append(char)
    parts.append("".join(current))
    return parts


def parse_segments(
    path: str, prefixes: tuple[str, ...] = ()
) -> list[tuple[str, str | None]]:
    """Parse a dotted path into ``(name, key)`` segments.

    ``key`` is ``None`` for a plain attribute, otherwise the named-object key or
    list index (as a string).

    Raises
    ------
    PathResolutionError
        If a segment is malformed.
    """
    cleaned = path.strip().lstrip(".")
    for prefix in prefixes:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix) :]
            break
    if not cleaned:
        return []
    segments: list[tuple[str, str | None]] = []
    for part in _split_dotted(cleaned):
        match = _SEGMENT_RE.fullmatch(part.strip())
        if not match:
            raise PathResolutionError(f"Malformed path segment {part!r} in {path!r}.")
        key = match.group("key")
        segments.append(
            (match.group("name"), _strip_quotes(key) if key is not None else None)
        )
    return segments


def resolve(root: Any, path: str, prefixes: tuple[str, ...] = ()) -> Any:
    """Resolve a dotted Python path against a settings root.

    Raises
    ------
    PathResolutionError
        If a segment cannot be resolved.
    """
    obj = root
    walked: list[str] = []
    for name, key in parse_segments(path, prefixes):
        walked.append(name if key is None else f"{name}[{key!r}]")
        try:
            obj = getattr(obj, name)
            if key is not None:
                obj = obj[int(key) if key.isdigit() else key]
        except Exception as err:  # noqa: BLE001
            raise PathResolutionError(
                f"Cannot resolve {'.'.join(walked)!r}: {err}"
            ) from err
    return obj


def _scheme_name(obj: Any, name_attr: str) -> Any:
    try:
        return getattr(obj, name_attr, None)
    except Exception:  # noqa: BLE001
        return None


def _child_by_scheme_name(obj: Any, segment: str, name_attr: str) -> Any:
    """Find the child of ``obj`` whose server-side name is ``segment``."""
    for py_name in list(getattr(obj, "child_names", None) or []) + list(
        getattr(obj, "command_names", None) or []
    ):
        try:
            child = getattr(obj, py_name)
        except Exception:  # noqa: BLE001  # nosec B112
            # An inactive sibling can raise on access; it is not this segment.
            continue
        if _scheme_name(child, name_attr) == segment:
            return child
    for guess in (segment.replace("-", "_"), segment.replace("-", "_").lower()):
        try:
            child = getattr(obj, guess, None)
        except Exception:  # noqa: BLE001  # nosec B112
            continue
        if child is not None:
            return child
    try:
        return obj[segment]
    except Exception as err:  # noqa: BLE001
        raise PathResolutionError(f"Cannot map segment {segment!r}.") from err


def resolve_scheme_path(root: Any, path: str, name_attr: str) -> Any:
    """Resolve a slash-separated server path against a settings root.

    Raises
    ------
    PathResolutionError
        If a segment cannot be resolved.
    """
    obj = root
    walked: list[str] = []
    for segment in (s for s in path.replace("\\", "/").split("/") if s):
        walked.append(segment)
        try:
            obj = _child_by_scheme_name(obj, segment, name_attr)
        except PathResolutionError as err:
            raise PathResolutionError(
                f"Cannot resolve {'/'.join(walked)!r}: {err}"
            ) from err
    return obj


def resolve_any(
    root: Any, path: str, *, prefixes: tuple[str, ...] = (), name_attr: str
) -> Any:
    """Resolve either a dotted Python path or a slash-separated server path.

    Raises
    ------
    PathResolutionError
        If the path cannot be resolved in either form.
    """
    if "/" in path or ("." not in path and "-" in path):
        return resolve_scheme_path(root, path, name_attr)
    try:
        return resolve(root, path, prefixes)
    except PathResolutionError:
        if "." not in path:
            return resolve_scheme_path(root, path, name_attr)
        raise
