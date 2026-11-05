# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
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

"""Narrow adapters over core PyFluent internals.

This is the **only** module in the package that reaches into private core
attributes (notably ``session._fluent_connection._error_state``). Keeping that
coupling in one place makes it reviewable and easy to adjust if core changes.

All helpers are defensive: they degrade gracefully (returning ``None`` / a
best-effort boolean) rather than raising on a session that does not expose a
given capability, so the runtime also works against mock sessions in tests and
over transports (REST) that lack the gRPC error-state stream.
"""

from __future__ import annotations

import re

from ansys.fluent.core.resilient.adapter import adapter_for
from ansys.fluent.core.resilient.exceptions import PathResolutionError

#: Matches a path segment with an optional ``["key"]`` / ``['key']`` / ``[index]``
#: suffix. Mirrors the addressing used across the settings knowledge base.
_SEGMENT_RE = re.compile(
    r"""(?P<name>[A-Za-z_][A-Za-z0-9_]*)
        (?:\[\s*(?P<key>"[^"]*"|'[^']*'|<[^>]*>|\d+)\s*\])?""",
    re.VERBOSE,
)

#: Fallback path prefixes (used when no session/adapter is available, e.g. when
#: parsing a bare path in isolation). Per-product prefixes come from the adapter.
_DEFAULT_PATH_PREFIXES = ("solver.settings.", "settings.", "solver.")


def settings_root(session):
    """Return the settings root for a session (delegates to the adapter).

    A bare settings tree (used in tests) is returned unchanged.
    """
    return adapter_for(session).settings_root(session)


def _strip_quotes(key: str) -> str:
    key = key.strip()
    if len(key) >= 2 and key[0] in "\"'" and key[-1] == key[0]:
        return key[1:-1]
    return key


def _prefixes_for(session) -> tuple[str, ...]:
    if session is None:
        return _DEFAULT_PATH_PREFIXES
    # Combine the adapter's prefixes with the defaults so a user path written
    # with any recognised prefix still resolves.
    return tuple(adapter_for(session).path_prefixes) + _DEFAULT_PATH_PREFIXES


def parse_segments(path: str, session=None) -> list[tuple[str, str | None]]:
    """Parse a dotted path into ``(name, key)`` segments.

    ``key`` is ``None`` for a plain attribute, the string key for a named
    object, or the raw index string for a list object. ``session`` (optional)
    selects the product's recognised path prefixes via its adapter.

    Raises
    ------
    PathResolutionError
        If any path segment is malformed.
    """
    cleaned = path.strip().lstrip(".")
    for prefix in _prefixes_for(session):
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix) :]
            break
    segments: list[tuple[str, str | None]] = []
    if not cleaned:
        return segments
    for part in cleaned.split("."):
        match = _SEGMENT_RE.fullmatch(part.strip())
        if not match:
            raise PathResolutionError(f"Malformed path segment {part!r} in {path!r}.")
        name = match.group("name")
        key = match.group("key")
        if key is not None:
            key = _strip_quotes(key)
        segments.append((name, key))
    return segments


def resolve(session, path: str):
    """Resolve a dotted path to a live settings object.

    Raises
    ------
    PathResolutionError
        If any segment cannot be resolved against the live tree.
    """
    obj = settings_root(session)
    walked: list[str] = []
    for name, key in parse_segments(path, session):
        walked.append(name if key is None else f"{name}[{key!r}]")
        try:
            obj = getattr(obj, name)
        except Exception as err:  # noqa: BLE001
            raise PathResolutionError(
                f"Cannot resolve {'.'.join(walked)!r} on the live session: {err}"
            ) from err
        if key is not None:
            if key.startswith("<") and key.endswith(">"):
                raise PathResolutionError(
                    f"Path {path!r} contains an unresolved placeholder {key!r}; "
                    "provide a concrete named-object key."
                )
            try:
                obj = obj[key]
            except Exception as err:  # noqa: BLE001
                raise PathResolutionError(
                    f"No instance {key!r} for collection {'.'.join(walked)!r}: "
                    f"{err}"
                ) from err
    return obj


def _scheme_name(child):
    """Return a child's scheme (server-side) name across products.

    Fluent exposes it as ``fluent_name``, CFX as ``cfx_name``; ``obj_name`` is a
    product-neutral fallback both provide.
    """
    for attr in ("fluent_name", "cfx_name", "obj_name"):
        val = getattr(child, attr, None)
        if val:
            return val
    return None


def _child_by_fluent_name(obj, segment: str):
    """Find a child of ``obj`` whose scheme name matches ``segment``.

    The settings service uses scheme paths (e.g. Fluent
    ``boundary-conditions`` / CFX ``FLOW``) while the live tree is navigated by
    Python names. This maps one scheme segment to the right child, trying, in
    order:

    * a child whose scheme name (fluent_name / cfx_name / obj_name) equals it,
    * the pythonized segment (hyphens/spaces -> underscores, lower-cased),
    * the segment as a named-object / list key.

    Returns the resolved child, or raises ``PathResolutionError``.
    """
    # 1. Match a child by its scheme name via the class metadata, if available.
    child_names = getattr(obj, "child_names", None) or []
    for py_name in child_names:
        try:
            child = getattr(obj, py_name)
            if _scheme_name(child) == segment:
                return child
        except Exception:  # noqa: BLE001  # nosec B112
            # An inactive child can raise InactiveObjectError on attribute access
            # or on scheme-name introspection; skip it -- it is not our segment.
            continue
    # Command names, too (for execute_cmd parents).
    command_names = getattr(obj, "command_names", None) or []
    for py_name in command_names:
        try:
            child = getattr(obj, py_name, None)
            if child is not None and _scheme_name(child) == segment:
                return child
        except Exception:  # noqa: BLE001  # nosec B112
            continue
    # 2. Pythonized attribute name (hyphens/spaces -> underscores, lower-cased).
    for guess in (
        segment.replace("-", "_"),
        segment.replace("-", "_").replace(" ", "_").lower(),
    ):
        try:
            child = getattr(obj, guess, None)
        except Exception:  # noqa: BLE001  # nosec B112
            # Attribute access on an inactive child may raise; treat as a miss.
            continue
        if child is not None:
            return child
    # 3. Named-object / list key (CFX keys like 'Flow Analysis 1' resolve here).
    try:
        return obj[segment]
    except Exception:  # noqa: BLE001  # nosec B110
        pass
    raise PathResolutionError(f"Cannot map scheme segment {segment!r}.")


def resolve_scheme_path(session, path: str):
    """Resolve a Fluent scheme path (slash-separated) to a live settings object.

    Used when the path originates from the settings service layer, which speaks
    scheme paths. Resolves segment-by-segment against the live tree using each
    object's own Fluent-name metadata, so named-object keys that contain hyphens
    (e.g. ``cold-inlet``) are handled correctly.
    """
    obj = settings_root(session)
    segments = [s for s in path.replace("\\", "/").split("/") if s]
    # Drop a leading scheme root if present.
    while segments and segments[0] in ("", "settings"):
        segments = segments[1:]
    walked: list[str] = []
    for segment in segments:
        walked.append(segment)
        try:
            obj = _child_by_fluent_name(obj, segment)
        except PathResolutionError as err:
            raise PathResolutionError(
                f"Cannot resolve scheme path {'/'.join(walked)!r} on the live "
                f"session: {err}"
            ) from err
    return obj


def resolve_any(session, path: str):
    """Resolve ``path`` whether it is a Python dotted path or a Fluent scheme path.

    Tries the dotted form first (``a.b["k"].c``); if that fails and the path looks
    like a scheme path (contains ``/`` or ``-``), falls back to
    :func:`resolve_scheme_path`.
    """
    try:
        return resolve(session, path)
    except PathResolutionError:
        if "/" in path or "-" in path:
            return resolve_scheme_path(session, path)
        raise


def resolve_parent(session, path: str):
    """Resolve the parent object and final segment name of a path.

    Useful for command invocation, where the final segment is the method name.

    Raises
    ------
    PathResolutionError
        If the path is empty or ends in an indexed segment.
    """
    segments = parse_segments(path, session)
    if not segments:
        raise PathResolutionError(f"Empty path: {path!r}.")
    leaf_name, leaf_key = segments[-1]
    if leaf_key is not None:
        raise PathResolutionError(
            f"Path {path!r} ends in an indexed segment; expected a method name."
        )
    parent_path = ".".join(
        name if key is None else f'{name}["{key}"]' for name, key in segments[:-1]
    )
    parent = resolve(session, parent_path) if parent_path else settings_root(session)
    return parent, leaf_name


def error_state(session):
    """Return the session's ``ErrorState`` object, or ``None`` (via the adapter)."""
    return adapter_for(session).error_state(session)


def is_fatal(session) -> bool:
    """Whether the server is in a fatal error state (via the adapter)."""
    return adapter_for(session).is_fatal(session)


def fatal_details(session) -> str | None:
    """Return the fatal-error details string, if any (via the adapter)."""
    return adapter_for(session).fatal_details(session)


def is_server_healthy(session) -> bool:
    """Best-effort health probe that never raises (via the adapter)."""
    return adapter_for(session).is_server_healthy(session)
