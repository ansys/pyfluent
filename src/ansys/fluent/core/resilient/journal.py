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

"""Operation journal for resilient mode.

The journal records the **operations** a resilient session performs -- not copies
of the Fluent state -- so a solver setup can be replayed/replicated with errors
already resolved. Each successful ``set`` is stored as a :class:`SetOp` carrying
the value that was read (``old_value``, via ``get_state``) and the value that was
ultimately applied (``new_value``); each command is stored as a :class:`CommandOp``.

A rejected ``set`` is undone by writing ``old_value`` back (``set_state``) -- the
last-good state -- and, when recoverable, redone by writing the repaired value.
This is the lightweight "store the code, not the state" model: one value per step,
not a full settings-tree snapshot.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Callable


@dataclass
class SetOp:
    """A recorded value-set operation (the undo value is the pre-set state)."""

    path: str
    old_value: object
    new_value: object
    fixes: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)

    kind: str = "set"

    def to_dict(self) -> dict:
        """Serialize this operation to a plain dict."""
        data = {
            "kind": self.kind,
            "path": self.path,
            "old_value": self.old_value,
            "new_value": self.new_value,
        }
        if self.fixes:
            data["fixes"] = list(self.fixes)
        return data


@dataclass
class CommandOp:
    """A recorded command invocation (replayed by re-running the command)."""

    path: str
    args: dict = field(default_factory=dict)
    irreversible: bool = False
    checkpoint_name: str | None = None
    created_at: float = field(default_factory=time.time)

    kind: str = "command"

    def to_dict(self) -> dict:
        """Serialize this operation to a plain dict."""
        data = {"kind": self.kind, "path": self.path, "args": dict(self.args)}
        if self.irreversible:
            data["irreversible"] = True
        if self.checkpoint_name:
            data["checkpoint"] = self.checkpoint_name
        return data


class Journal:
    """An append-only timeline of operations with undo / redo cursors.

    The journal is a single global history for the whole run (start to end). It
    stores operations the session has successfully applied so the setup can be
    replayed. ``undo`` steps the cursor back over the most recent operation and
    restores its recorded ``old_value`` on the live tree; ``redo`` re-applies the
    operation. Listeners registered with :meth:`on_event` are notified of
    ``record`` / ``undo`` / ``redo`` so callers (examples, logs) can surface them.
    """

    def __init__(self, restore: Callable[[str, object], None]):
        #: Callback used to write a value back to the live tree, ``(path, value)``.
        self._restore = restore
        self._ops: list = []
        #: Index of the next op to undo (one past the last live op).
        self._cursor = 0
        self._listeners: list[Callable[[str, object], None]] = []

    # -- notifications ----------------------------------------------------

    def on_event(self, listener: Callable[[str, object], None]) -> None:
        """Register a ``(event_name, op)`` listener (``record`` / ``undo`` / ``redo``)."""
        self._listeners.append(listener)

    def _notify(self, event_name: str, op) -> None:
        for listener in list(self._listeners):
            try:
                listener(event_name, op)
            except Exception:  # noqa: BLE001  # nosec B112
                continue

    # -- recording --------------------------------------------------------

    def record(self, op) -> None:
        """Append a successful operation to the timeline (truncating any redo tail)."""
        # A new recorded op invalidates anything that had been undone.
        del self._ops[self._cursor :]
        self._ops.append(op)
        self._cursor = len(self._ops)
        self._notify("record", op)

    # -- undo / redo ------------------------------------------------------

    def can_undo(self) -> bool:
        """Whether there is an operation to undo."""
        return self._cursor > 0

    def can_redo(self) -> bool:
        """Whether there is an undone operation to redo."""
        return self._cursor < len(self._ops)

    def undo(self) -> object | None:
        """Undo the most recent live operation, restoring its ``old_value``.

        Returns the undone op, or ``None`` if there is nothing to undo.
        """
        if not self.can_undo():
            return None
        self._cursor -= 1
        op = self._ops[self._cursor]
        if isinstance(op, SetOp):
            self._restore(op.path, op.old_value)
        self._notify("undo", op)
        return op

    def redo(self) -> object | None:
        """Redo the most recently undone operation, re-applying its ``new_value``.

        Returns the redone op, or ``None`` if there is nothing to redo.
        """
        if not self.can_redo():
            return None
        op = self._ops[self._cursor]
        self._cursor += 1
        if isinstance(op, SetOp):
            self._restore(op.path, op.new_value)
        self._notify("redo", op)
        return op

    # -- introspection ----------------------------------------------------

    @property
    def operations(self) -> list:
        """A copy of the recorded operations (live portion + undone tail)."""
        return list(self._ops)

    @property
    def live_operations(self) -> list:
        """The operations currently applied (up to the undo cursor)."""
        return list(self._ops[: self._cursor])

    def replay_script(self) -> list[dict]:
        """The live operations as plain dicts -- the replayable setup journal."""
        return [op.to_dict() for op in self.live_operations]
