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

"""Two-tier checkpoint manager with a unified undo / redo stack.

A single undo stack interleaves both checkpoint tiers in creation order:

* **settings** entries restore reversible state via ``set_state``;
* **file** entries reload a case/data artifact via ``read_case_data``.

Undo is implemented as *capture-current-then-restore-past*: before restoring a
popped entry, the manager captures the present state (same tier) and pushes it
onto the redo stack, so every undo is itself redoable. This keeps the two tiers
symmetric -- a settings undo snapshots the present via ``get_state``; a file undo
writes the present via ``write_case_data``.
"""

from __future__ import annotations

from ansys.fluent.core.resilient import snapshot
from ansys.fluent.core.resilient.exceptions import CheckpointError
from ansys.fluent.core.resilient.filecheck import (
    FileCheckpointConfig,
    FileCheckpointStore,
)
from ansys.fluent.core.resilient.types import CheckpointKind, UndoEntry

#: Default (Fluent) leaf command names that are irreversible via ``set_state``
#: and therefore warrant a file checkpoint before they run. Products override via
#: the adapter's ``irreversible_leaves``.
IRREVERSIBLE_LEAVES = frozenset(
    {
        "iterate",
        "calculate",
        "dual_time_iterate",
        "read_case",
        "read_case_data",
        "read_data",
        "read",
    }
)


def is_irreversible(path: str, session=None) -> bool:
    """Whether a command path refers to an irreversible operation.

    When a ``session`` is given, the product adapter's ``irreversible_leaves`` is
    used; otherwise the Fluent default set applies.
    """
    if session is not None:
        from ansys.fluent.core.resilient.adapter import adapter_for

        adapter = adapter_for(session)
        if adapter.irreversible_leaves:
            return adapter.is_irreversible(path)
    leaf = path.strip().rstrip(")").split("(")[0].split(".")[-1]
    return leaf in IRREVERSIBLE_LEAVES


class CheckpointManager:
    """Manage two-tier checkpoints and a unified undo / redo stack."""

    def __init__(
        self,
        session,
        *,
        file_config: FileCheckpointConfig | None = None,
        max_depth: int = 50,
        adapter=None,
    ):
        self.session = session
        self.max_depth = max_depth
        if adapter is None:
            from ansys.fluent.core.resilient.adapter import adapter_for

            adapter = adapter_for(session)
        self._adapter = adapter
        self._file_store = FileCheckpointStore(file_config)
        self._undo: list[UndoEntry] = []
        self._redo: list[UndoEntry] = []

    def _file_write(self, name: str) -> UndoEntry:
        """Write a file-tier checkpoint via the adapter (or the default store)."""
        writer = getattr(self._adapter, "write_file_checkpoint", None)
        if callable(writer):
            return writer(self.session, name, self._file_store)
        return self._file_store.write(self.session, name)

    def _file_restore(self, entry: UndoEntry) -> None:
        """Restore a file-tier checkpoint via the adapter (or the default store)."""
        restorer = getattr(self._adapter, "restore_file_checkpoint", None)
        if callable(restorer):
            restorer(self.session, entry, self._file_store)
        else:
            self._file_store.restore(self.session, entry)

    def rebind(self, session) -> None:
        """Point the manager at a new session (after a failover)."""
        self.session = session

    # -- taking checkpoints ----------------------------------------------

    def checkpoint_settings(
        self, name: str, paths=None, *, clear_redo: bool = True
    ) -> UndoEntry:
        """Push a settings snapshot onto the undo stack."""
        entry = snapshot.capture_settings(self.session, paths, name)
        self._push_undo(entry, clear_redo=clear_redo)
        return entry

    def checkpoint_file(
        self, name: str, reason: str | None = None, *, clear_redo: bool = True
    ) -> UndoEntry:
        """Push a file checkpoint (case/data) onto the undo stack."""
        entry = self._file_write(name)
        entry.reason = reason
        self._push_undo(entry, clear_redo=clear_redo)
        return entry

    def checkpoint_auto(
        self, name: str, *, before_irreversible: bool, paths=None
    ) -> UndoEntry:
        """Policy helper: file checkpoint before irreversible ops, else settings."""
        if before_irreversible:
            return self.checkpoint_file(name, reason="pre-irreversible")
        return self.checkpoint_settings(name, paths)

    # -- undo / redo ------------------------------------------------------

    def undo(self) -> UndoEntry:
        """Undo the newest checkpoint, making it redoable.

        Captures the current state (same tier) onto the redo stack, then restores
        the popped entry.
        """
        if not self._undo:
            raise CheckpointError("Nothing to undo.")
        entry = self._undo.pop()
        redo_entry = self._capture_current(entry, name=f"redo:{entry.name}")
        self._apply(entry)
        self._redo.append(redo_entry)
        return entry

    def redo(self) -> UndoEntry:
        """Redo the most recently undone checkpoint."""
        if not self._redo:
            raise CheckpointError("Nothing to redo.")
        entry = self._redo.pop()
        undo_entry = self._capture_current(entry, name=f"undo:{entry.name}")
        self._apply(entry)
        self._undo.append(undo_entry)
        return entry

    def rewind_to(self, name: str) -> list[UndoEntry]:
        """Undo repeatedly until the named checkpoint has been restored."""
        if not any(e.name == name for e in self._undo):
            raise CheckpointError(f"No checkpoint named {name!r} on the undo stack.")
        undone: list[UndoEntry] = []
        while self._undo:
            entry = self.undo()
            undone.append(entry)
            if entry.name == name:
                break
        return undone

    def last_good(self) -> UndoEntry | None:
        """Newest checkpoint on the undo stack (used for failover replay)."""
        return self._undo[-1] if self._undo else None

    def newest_file_checkpoint(self) -> UndoEntry | None:
        """Newest FILE checkpoint, if any (the authoritative replay base)."""
        for entry in reversed(self._undo):
            if entry.kind is CheckpointKind.FILE:
                return entry
        return None

    @property
    def undo_stack(self) -> list[UndoEntry]:
        """A copy of the current undo stack (oldest first)."""
        return list(self._undo)

    @property
    def redo_stack(self) -> list[UndoEntry]:
        """A copy of the current redo stack."""
        return list(self._redo)

    # -- internals --------------------------------------------------------

    def _capture_current(self, like: UndoEntry, name: str) -> UndoEntry:
        if like.kind is CheckpointKind.SETTINGS:
            return snapshot.capture_settings(self.session, like.paths or None, name)
        return self._file_write(name)

    def _apply(self, entry: UndoEntry) -> None:
        if entry.kind is CheckpointKind.SETTINGS:
            snapshot.restore_settings(self.session, entry)
        else:
            self._file_restore(entry)

    def replay(self, entry: UndoEntry) -> None:
        """Apply a checkpoint onto the current session (used by failover)."""
        self._apply(entry)

    def _push_undo(self, entry: UndoEntry, *, clear_redo: bool) -> None:
        self._undo.append(entry)
        if clear_redo:
            self._redo.clear()
        if len(self._undo) > self.max_depth:
            self._undo.pop(0)
