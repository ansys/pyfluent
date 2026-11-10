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

"""Shared vocabulary of the resilient engine (standard library only)."""

from __future__ import annotations

from dataclasses import dataclass, field
import enum
import time
from typing import Any


class ErrorCategory(enum.Enum):
    """Machine-readable classification of an error raised by a settings call."""

    #: The target is read-only.
    READ_ONLY = "read_only"
    #: The server is in a fatal state or no longer serving.
    FATAL = "fatal"
    #: A clean stop of an interruptible (solve) command.
    BENIGN_INTERRUPT = "benign_interrupt"
    #: None of the above.
    UNKNOWN = "unknown"


class Severity(enum.Enum):
    """How the engine responds to a classified error."""

    #: The session is unusable; fail over to a standby session if one exists.
    CATASTROPHIC = "catastrophic"
    #: Not an error (clean solver stop).
    BENIGN = "benign"
    #: Not catastrophic; the original error is raised unchanged.
    HARD = "hard"


@dataclass(frozen=True)
class Classification:
    """Result of classifying an exception."""

    category: ErrorCategory
    severity: Severity
    message: str
    details: str | None = None

    @property
    def catastrophic(self) -> bool:
        """Whether this error makes the session unusable."""
        return self.severity is Severity.CATASTROPHIC

    @property
    def benign(self) -> bool:
        """Whether this is a clean solver stop rather than an error."""
        return self.severity is Severity.BENIGN


@dataclass
class StepOutcome:
    """Outcome of one intercepted settings write or command."""

    path: str
    ok: bool
    old_value: Any = None
    new_value: Any = None
    result: Any = None
    rolled_back: bool = False
    failed_over: bool = False
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return the non-empty fields of the outcome as a plain dictionary."""
        data: dict[str, Any] = {"path": self.path, "ok": self.ok}
        for name in ("old_value", "new_value", "result", "error"):
            value = getattr(self, name)
            if value is not None:
                data[name] = value
        if self.rolled_back:
            data["rolled_back"] = True
        if self.failed_over:
            data["failed_over"] = True
        return data


@dataclass
class Checkpoint:
    """A restorable checkpoint written by the product (for example a case file)."""

    name: str
    path: str
    include_data: bool
    reason: str | None = None
    #: Journal position when the checkpoint was taken. Journal operations with a
    #: sequence number at or above this value happened after the checkpoint.
    journal_seq: int = 0
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        """Return the checkpoint metadata as a plain dictionary."""
        return {
            "name": self.name,
            "path": self.path,
            "include_data": self.include_data,
            "reason": self.reason,
            "journal_seq": self.journal_seq,
            "created_at": self.created_at,
        }


class EventKind(str, enum.Enum):
    """Kinds of events reported by a resilient session."""

    #: A checkpoint was written.
    CHECKPOINT = "checkpoint"
    #: The session was restored to a checkpoint.
    ROLLBACK = "rollback"
    #: A journaled settings write was undone.
    UNDO = "undo"
    #: A journaled settings write was redone.
    REDO = "redo"
    #: A standby session took over from a session that died.
    FAILOVER = "failover"


@dataclass(frozen=True)
class ResilientEvent:
    """An event reported to listeners registered with ``on_event``."""

    kind: EventKind
    message: str
    path: str | None = None
    data: dict[str, Any] = field(default_factory=dict)


def brief(value: Any) -> Any:
    """Return a compact, printable preview of a settings value."""
    if isinstance(value, (str, int, float, bool, type(None))):
        return value
    if isinstance(value, dict):
        return f"<dict: {len(value)} keys>"
    if isinstance(value, (list, tuple)):
        return f"<{type(value).__name__}: {len(value)} items>"
    return repr(value)
