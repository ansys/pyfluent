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

"""Settings-tier snapshot / restore.

Captures the state of one or more settings subtrees via bulk ``get_state()`` and
writes it back via ``set_state()``. This is the reversible checkpoint tier; it
operates on the live settings tree and is therefore transport-agnostic.

Restore uses :func:`safe_set_state`, a clean reimplementation of
``Solver._set_state_safe``: on a ``RuntimeError`` it recurses into a group /
named object child-by-child so that one leaf that refuses to apply (e.g. it is
inactive under the restored model state) does not abort the whole restore.
"""

from __future__ import annotations

from ansys.fluent.core.resilient import _compat
from ansys.fluent.core.resilient.exceptions import PathResolutionError
from ansys.fluent.core.resilient.types import CheckpointKind, StepOutcome, UndoEntry

#: The key used for a whole-tree snapshot.
ROOT_KEY = "<root>"


def capture_settings(session, paths=None, name: str = "checkpoint") -> UndoEntry:
    """Capture the state of the given paths (or the whole settings root).

    Parameters
    ----------
    session :
        A live Solver / Meshing session (or a settings tree in tests).
    paths : list[str], optional
        Dotted paths to capture. ``None`` captures the entire settings root,
        the broadest checkpoint.
    name : str
        A label for the resulting undo entry.

    Never raises for a bad path; unresolvable / unreadable paths are recorded in
    the entry's ``errors`` map so the caller can inspect them.
    """
    entry = UndoEntry(
        kind=CheckpointKind.SETTINGS, name=name, states={}, paths=list(paths or [])
    )
    if not paths:
        root = _compat.settings_root(session)
        try:
            entry.states[ROOT_KEY] = root.get_state()
        except Exception as err:  # noqa: BLE001
            entry.errors[ROOT_KEY] = str(err)
        return entry
    for path in paths:
        try:
            entry.states[path] = _compat.resolve(session, path).get_state()
        except PathResolutionError as err:
            entry.errors[path] = str(err)
        except Exception as err:  # noqa: BLE001
            entry.errors[path] = str(err)
    return entry


def restore_settings(session, entry: UndoEntry) -> list[StepOutcome]:
    """Write an entry's captured states back to the live session.

    Returns a per-path list of :class:`StepOutcome`. Tolerant of partial
    failures (each path is attempted independently via :func:`safe_set_state`).
    """
    outcomes: list[StepOutcome] = []
    for path, state in (entry.states or {}).items():
        try:
            if path == ROOT_KEY:
                target = _compat.settings_root(session)
            else:
                target = _compat.resolve(session, path)
            safe_set_state(target, state)
            outcomes.append(StepOutcome(path=path, ok=True, new_value=_brief(state)))
        except Exception as err:  # noqa: BLE001
            outcomes.append(StepOutcome(path=path, ok=False, error=str(err)))
    return outcomes


def safe_set_state(obj, state) -> None:
    """Set state, recursing child-by-child on failure for container objects.

    Mirrors ``Solver._set_state_safe``: if a bulk ``set_state`` raises
    ``RuntimeError`` and the object is a mapping-like container whose state is a
    dict, each child is set independently so one bad leaf does not abort the
    whole restore. Non-container leaves re-raise.

    Raises
    ------
    RuntimeError
        If the object is not a dict-stated container and its ``set_state`` fails.
    """
    try:
        obj.set_state(state)
        return
    except RuntimeError:
        if not isinstance(state, dict):
            raise
    # Container fallback: apply children one at a time, best-effort.
    get_item = getattr(obj, "__getitem__", None)
    for child_name, child_state in state.items():
        child = None
        if callable(get_item):
            try:
                child = obj[child_name]
            except Exception:  # noqa: BLE001
                child = None
        if child is None:
            child = getattr(obj, child_name, None)
        if child is None:
            continue
        try:
            safe_set_state(child, child_state)
        except Exception:  # noqa: BLE001  # nosec B112
            # Best-effort: skip a child that cannot be restored in this state.
            continue


def _brief(state) -> object:
    """A compact, serializable preview of a captured state value."""
    if isinstance(state, (str, int, float, bool, type(None))):
        return state
    if isinstance(state, dict):
        return f"<dict:{len(state)} keys>"
    if isinstance(state, (list, tuple)):
        return f"<{type(state).__name__}:{len(state)}>"
    return repr(state)
