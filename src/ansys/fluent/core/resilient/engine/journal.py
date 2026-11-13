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

"""The operation journal: every state-changing settings call, in order.

The journal records *operations* (value writes, commands and object changes),
not copies of the server state. It serves two purposes:

* **undo / redo** of value writes, using the value read just before each write;
* **catching up** a standby session that is not up to date with the active
  session, starting from the newest checkpoint.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import threading
import time
from typing import Any, Callable, ClassVar

from .exceptions import ResilientError


@dataclass
class SetOp:
    """A value written with ``set_var``."""

    kind: ClassVar[str] = "set"

    path: str
    new_value: Any
    old_value: Any = None
    #: Whether ``old_value`` was read before the write (required for undo).
    old_value_known: bool = False
    seq: int = -1
    created_at: float = field(default_factory=time.time)

    def describe(self) -> str:
        """Return a one-line description of the operation."""
        return f"set {self.path} = {self.new_value!r}"

    def to_dict(self) -> dict[str, Any]:
        """Return the operation as a plain dictionary."""
        data = {"kind": self.kind, "seq": self.seq, "path": self.path}
        data["new_value"] = self.new_value
        if self.old_value_known:
            data["old_value"] = self.old_value
        return data


@dataclass
class CommandOp:
    """A command executed with ``execute_cmd``."""

    kind: ClassVar[str] = "command"

    path: str
    command: str
    args: dict[str, Any] = field(default_factory=dict)
    irreversible: bool = False
    checkpoint: str | None = None
    seq: int = -1
    created_at: float = field(default_factory=time.time)

    @property
    def full_path(self) -> str:
        """Return the command path including the command name."""
        return f"{self.path}/{self.command}" if self.path else self.command

    def describe(self) -> str:
        """Return a one-line description of the operation."""
        return f"command {self.full_path}"

    def to_dict(self) -> dict[str, Any]:
        """Return the operation as a plain dictionary."""
        data = {
            "kind": self.kind,
            "seq": self.seq,
            "path": self.path,
            "command": self.command,
            "args": dict(self.args),
        }
        if self.irreversible:
            data["irreversible"] = True
        if self.checkpoint:
            data["checkpoint"] = self.checkpoint
        return data


@dataclass
class ObjectOp:
    """A structural change: ``create``, ``delete``, ``rename`` or a list resize."""

    kind: ClassVar[str] = "object"

    method: str
    path: str
    args: tuple[Any, ...] = ()
    seq: int = -1
    created_at: float = field(default_factory=time.time)

    def describe(self) -> str:
        """Return a one-line description of the operation."""
        return f"{self.method} {self.path} {list(self.args)}"

    def to_dict(self) -> dict[str, Any]:
        """Return the operation as a plain dictionary."""
        return {
            "kind": self.kind,
            "seq": self.seq,
            "method": self.method,
            "path": self.path,
            "args": list(self.args),
        }


Operation = SetOp | CommandOp | ObjectOp


class Journal:
    """Ordered, bounded record of state-changing operations with undo / redo.

    Parameters
    ----------
    max_ops : int, optional
        Maximum number of operations kept. When exceeded, the oldest operations
        are dropped (replay from before that point is then impossible and a
        failover requires a newer checkpoint).
    """

    def __init__(self, *, max_ops: int = 10_000):
        self._max_ops = max_ops
        self._ops: list[Operation] = []
        #: Number of live operations (``_ops[_cursor:]`` have been undone).
        self._cursor = 0
        self._next_seq = 0
        #: Sequence number of the oldest operation still held.
        self._first_seq = 0
        self._lock = threading.RLock()

    # -- recording -------------------------------------------------------------

    @property
    def next_seq(self) -> int:
        """Sequence number the next recorded operation receives."""
        return self._next_seq

    def record(self, op: Operation) -> Operation:
        """Append an operation, discarding any undone operations after the cursor."""
        with self._lock:
            del self._ops[self._cursor :]
            op.seq = self._next_seq
            self._next_seq += 1
            self._ops.append(op)
            if len(self._ops) > self._max_ops:
                dropped = len(self._ops) - self._max_ops
                del self._ops[:dropped]
            self._cursor = len(self._ops)
            self._first_seq = self._ops[0].seq if self._ops else self._next_seq
            return op

    # -- undo / redo -------------------------------------------------------------

    def can_undo(self) -> bool:
        """Return whether there is an operation to undo."""
        return self._cursor > 0

    def can_redo(self) -> bool:
        """Return whether there is an undone operation to redo."""
        return self._cursor < len(self._ops)

    def undo(self, write: Callable[[str, Any], None]) -> SetOp:
        """Undo the most recent value write by writing back its previous value.

        Raises
        ------
        ResilientError
            If there is nothing to undo, if the most recent operation is not a
            value write, or if its previous value was not captured.
        """
        with self._lock:
            if not self.can_undo():
                raise ResilientError("Nothing to undo.")
            op = self._ops[self._cursor - 1]
            if not isinstance(op, SetOp):
                raise ResilientError(
                    f"Cannot undo '{op.describe()}': only value writes can be undone. "
                    "Use rollback() to return to a checkpoint."
                )
            if not op.old_value_known:
                raise ResilientError(
                    f"Cannot undo '{op.describe()}': its previous value was not "
                    "captured."
                )
            write(op.path, op.old_value)
            self._cursor -= 1
            return op

    def redo(self, write: Callable[[str, Any], None]) -> SetOp:
        """Re-apply the most recently undone value write.

        Raises
        ------
        ResilientError
            If there is nothing to redo.
        """
        with self._lock:
            if not self.can_redo():
                raise ResilientError("Nothing to redo.")
            op = self._ops[self._cursor]
            write(op.path, op.new_value)
            self._cursor += 1
            return op

    # -- replay and truncation -------------------------------------------------

    def live_since(self, seq: int) -> list[Operation]:
        """Return the live operations with a sequence number of at least ``seq``.

        Raises
        ------
        ResilientError
            If operations after ``seq`` were already dropped from the journal.
        """
        with self._lock:
            if seq < self._first_seq and self._next_seq > seq:
                raise ResilientError(
                    "The journal no longer holds every operation since the last "
                    "checkpoint (journal_max_ops was exceeded)."
                )
            return [op for op in self._ops[: self._cursor] if op.seq >= seq]

    def truncate(self, seq: int) -> None:
        """Forget every operation with a sequence number of at least ``seq``."""
        with self._lock:
            self._ops = [op for op in self._ops if op.seq < seq]
            self._cursor = min(self._cursor, len(self._ops))

    # -- introspection -----------------------------------------------------------

    @property
    def operations(self) -> list[Operation]:
        """Return the live operations (oldest first)."""
        with self._lock:
            return list(self._ops[: self._cursor])

    def to_script(self) -> list[dict[str, Any]]:
        """Return the live operations as plain dictionaries."""
        return [op.to_dict() for op in self.operations]

    def __len__(self) -> int:
        return self._cursor
