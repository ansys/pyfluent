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

"""Shared vocabulary for the resilient execution runtime.

These enums and dataclasses are deliberately dependency-free (standard library
only) so they can be used by every other module in the package and asserted
against in unit tests without a live Fluent session.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import enum
import time


class ErrorCategory(enum.Enum):
    """A stable, machine-readable classification of a caught error.

    The category drives whether the runtime attempts an automatic repair
    (recoverable), fails over to a standby session (fatal), treats the error as
    a clean solver stop (benign interrupt), or gives up on the single step.
    """

    #: Target object is inactive in the current model state (recoverable:
    #: enable the governing model / assign the zone type, then retry).
    INACTIVE_TARGET = "inactive_target"
    #: Numeric value outside the live ``[min, max]`` bounds (recoverable: clamp).
    OUT_OF_RANGE = "out_of_range"
    #: Value not in the live ``allowed_values`` (recoverable: snap to nearest).
    WRONG_VALUE = "wrong_value"
    #: Value of the wrong Python type (recoverable-ish: coerce when safe).
    WRONG_TYPE = "wrong_type"
    #: Target is read-only; cannot be set at all (hard, not catastrophic).
    READ_ONLY = "read_only"
    #: The Fluent server is in a fatal state; the session is unusable.
    FATAL = "fatal"
    #: A clean solver stop / interrupt (``RuntimeError("()")``); not an error.
    BENIGN_INTERRUPT = "benign_interrupt"
    #: Could not be classified into any of the above.
    UNKNOWN = "unknown"


class Severity(enum.Enum):
    """How the runtime should respond to a classified error."""

    #: Session unusable -> fail over to a standby and replay from checkpoint.
    CATASTROPHIC = "catastrophic"
    #: The resolver can usually repair this and retry.
    RECOVERABLE = "recoverable"
    #: Clean stop / interrupt; treat the step as a (non-)success without retry.
    BENIGN = "benign"
    #: Non-catastrophic but unfixable by the resolver (e.g. read-only).
    HARD = "hard"


class CheckpointKind(enum.Enum):
    """Which tier a checkpoint / undo entry belongs to."""

    #: In-memory settings snapshot captured via ``get_state()``.
    SETTINGS = "settings"
    #: Case/data file written to disk via ``file.write_case_data``.
    FILE = "file"


#: Categories an agent / the resolver can usually repair and retry.
RECOVERABLE_CATEGORIES = frozenset(
    {
        ErrorCategory.INACTIVE_TARGET,
        ErrorCategory.OUT_OF_RANGE,
        ErrorCategory.WRONG_VALUE,
        ErrorCategory.WRONG_TYPE,
    }
)


@dataclass(frozen=True)
class Classification:
    """The result of classifying a caught exception."""

    category: ErrorCategory
    severity: Severity
    message: str
    details: str | None = None

    @property
    def recoverable(self) -> bool:
        """Whether the resolver can usually repair this and retry."""
        return self.severity is Severity.RECOVERABLE

    @property
    def catastrophic(self) -> bool:
        """Whether this requires a failover to a standby session."""
        return self.severity is Severity.CATASTROPHIC

    def to_dict(self) -> dict:
        """Serialize this classification to a plain dict."""
        data = {
            "category": self.category.value,
            "severity": self.severity.value,
            "message": self.message,
            "recoverable": self.recoverable,
            "catastrophic": self.catastrophic,
        }
        if self.details:
            data["details"] = self.details
        return data


@dataclass
class Fix:
    """A proposed repair for a recoverable error.

    ``pre_mutations`` are ``(path, value)`` pairs to apply *before* re-attempting
    the original set (e.g. enabling a governing model). ``new_value`` replaces the
    original value when the fix adjusts it (clamp / nearest-allowed / coerce).
    """

    kind: str
    description: str
    pre_mutations: list[tuple[str, object]] = field(default_factory=list)
    new_value: object | None = None

    def to_dict(self) -> dict:
        """Serialize this fix to a plain dict."""
        data = {"kind": self.kind, "description": self.description}
        if self.pre_mutations:
            data["pre_mutations"] = list(self.pre_mutations)
        if self.new_value is not None:
            data["new_value"] = self.new_value
        return data


@dataclass
class StepOutcome:
    """The outcome of applying a single set / command through the runtime."""

    path: str
    ok: bool
    old_value: object | None = None
    new_value: object | None = None
    result: object | None = None
    attempts: int = 1
    fixes_applied: list[str] = field(default_factory=list)
    failed_over: bool = False
    error: str | None = None

    def to_dict(self) -> dict:
        """Serialize this outcome to a plain dict."""
        data = {"path": self.path, "ok": self.ok, "attempts": self.attempts}
        if self.old_value is not None:
            data["old_value"] = self.old_value
        if self.new_value is not None:
            data["new_value"] = self.new_value
        if self.result is not None:
            data["result"] = self.result
        if self.fixes_applied:
            data["fixes_applied"] = list(self.fixes_applied)
        if self.failed_over:
            data["failed_over"] = True
        if self.error:
            data["error"] = self.error
        return data


@dataclass
class UndoEntry:
    """A single entry on the unified undo / redo stack.

    An entry is self-describing: ``kind`` tells the checkpoint manager how to
    restore it. A ``SETTINGS`` entry carries captured ``states`` keyed by path
    (``"<root>"`` for a whole-tree snapshot); a ``FILE`` entry carries the path
    of a written case/data artifact to be reloaded via ``read_case_data``.
    """

    kind: CheckpointKind
    name: str
    created_at: float = field(default_factory=time.time)
    # SETTINGS tier:
    states: dict | None = None
    paths: list[str] = field(default_factory=list)
    errors: dict = field(default_factory=dict)
    # FILE tier:
    case_data_path: str | None = None
    data: bool = True
    reason: str | None = None

    def to_dict(self) -> dict:
        """Serialize this entry's metadata to a plain dict."""
        data: dict = {
            "kind": self.kind.value,
            "name": self.name,
            "created_at": self.created_at,
        }
        if self.kind is CheckpointKind.SETTINGS:
            data["paths"] = self.paths
            data["captured"] = sorted((self.states or {}).keys())
            if self.errors:
                data["errors"] = self.errors
        else:
            data["case_data_path"] = self.case_data_path
            data["data"] = self.data
            if self.reason:
                data["reason"] = self.reason
        return data
