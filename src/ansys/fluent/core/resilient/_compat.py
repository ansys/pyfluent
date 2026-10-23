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

from ansys.fluent.core.resilient.exceptions import PathResolutionError

#: Matches a path segment with an optional ``["key"]`` / ``['key']`` / ``[index]``
#: suffix. Mirrors the addressing used across the settings knowledge base.
_SEGMENT_RE = re.compile(
    r"""(?P<name>[A-Za-z_][A-Za-z0-9_]*)
        (?:\[\s*(?P<key>"[^"]*"|'[^']*'|<[^>]*>|\d+)\s*\])?""",
    re.VERBOSE,
)

#: Prefixes a user may prepend to a path; stripped before walking the tree.
_PATH_PREFIXES = ("solver.settings.", "settings.", "solver.")


def settings_root(session):
    """Return ``session.settings`` if present, else the object itself.

    A bare settings tree (used in tests) is returned unchanged.
    """
    settings = getattr(session, "settings", None)
    return settings if settings is not None else session


def _strip_quotes(key: str) -> str:
    key = key.strip()
    if len(key) >= 2 and key[0] in "\"'" and key[-1] == key[0]:
        return key[1:-1]
    return key


def parse_segments(path: str) -> list[tuple[str, str | None]]:
    """Parse a dotted path into ``(name, key)`` segments.

    ``key`` is ``None`` for a plain attribute, the string key for a named
    object, or the raw index string for a list object.

    Raises
    ------
    PathResolutionError
        If any path segment is malformed.
    """
    cleaned = path.strip().lstrip(".")
    for prefix in _PATH_PREFIXES:
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
    for name, key in parse_segments(path):
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


def _child_by_fluent_name(obj, segment: str):
    """Find a child of ``obj`` whose Fluent (scheme) name matches ``segment``.

    The settings service uses scheme paths (slash-separated, hyphenated, e.g.
    ``boundary-conditions``) while the live tree is navigated by Python names
    (dotted, underscored, e.g. ``boundary_conditions``). This maps one scheme
    segment to the right child, trying, in order:

    * a child whose ``fluent_name`` equals the segment,
    * the pythonized segment (hyphens -> underscores) as an attribute,
    * the segment as a named-object / list key.

    Returns the resolved child, or raises ``PathResolutionError``.
    """
    # 1. Match a child by its Fluent name via the class metadata, if available.
    child_names = getattr(obj, "child_names", None) or []
    for py_name in child_names:
        try:
            child = getattr(obj, py_name)
        except Exception:  # noqa: BLE001  # nosec B112
            continue
        if getattr(child, "fluent_name", None) == segment:
            return child
    # Command names, too (for execute_cmd parents).
    command_names = getattr(obj, "command_names", None) or []
    for py_name in command_names:
        child = getattr(obj, py_name, None)
        if child is not None and getattr(child, "fluent_name", None) == segment:
            return child
    # 2. Pythonized attribute name (hyphen -> underscore).
    py_guess = segment.replace("-", "_")
    child = getattr(obj, py_guess, None)
    if child is not None:
        return child
    # 3. Named-object / list key.
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
    segments = parse_segments(path)
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
    """Return the session's ``ErrorState`` object, or ``None`` if unavailable.

    Reaches ``session._fluent_connection._error_state``. Guarded so that mock
    sessions and transports without the gRPC error-state stream return ``None``.
    """
    connection = getattr(session, "_fluent_connection", None)
    if connection is None:
        return None
    return getattr(connection, "_error_state", None)


def is_fatal(session) -> bool:
    """Whether the Fluent server is in a fatal error state.

    Authoritative post-hoc check: the ``FATAL_ERROR`` event sets the shared
    ``ErrorState`` to ``"fatal"`` and every subsequent RPC is then refused.
    """
    state = error_state(session)
    return bool(state is not None and getattr(state, "name", "") == "fatal")


def fatal_details(session) -> str | None:
    """Return the fatal-error details string, if any."""
    state = error_state(session)
    if state is None:
        return None
    return getattr(state, "details", None) or None


def is_server_healthy(session) -> bool:
    """Best-effort health probe that never raises.

    Uses ``BaseSession._is_server_healthy()`` / ``is_active()`` when present and
    falls back to ``True`` for objects (e.g. mock trees) that expose neither.
    """
    for attr in ("_is_server_healthy", "is_active"):
        probe = getattr(session, attr, None)
        if callable(probe):
            try:
                return bool(probe())
            except Exception:  # noqa: BLE001
                return False
    return True
