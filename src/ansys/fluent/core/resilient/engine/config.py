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

"""Configuration of resilient mode."""

from __future__ import annotations

from dataclasses import dataclass, field
import enum
import os
from typing import Any, Callable

from .types import ActivationCandidate


class RecoveryPolicy(str, enum.Enum):
    """What resilient mode may do when the server rejects a value."""

    #: Never change a value: the original error propagates unchanged. Journaling,
    #: checkpoints, rollback and failover still apply.
    STRICT = "strict"
    #: Repair the value (clamp, snap to the nearest allowed value, or coerce a
    #: numeric string), apply it, and emit a ``ResilientRecoveryWarning``.
    WARN = "warn"
    #: Repair and apply the value; only log the repair.
    SILENT = "silent"


@dataclass
class CheckpointConfig:
    """Where and how checkpoints are written.

    Parameters
    ----------
    directory : str or os.PathLike, optional
        Directory for checkpoint files. For a server that shares the client file
        system, the default is ``resilient_checkpoints/<run-id>`` under the
        current working directory. For a remote or containerized server, the
        default is the server working directory.
    keep_last : int, optional
        Number of most recent checkpoints to keep. Older ones are deleted when the
        client can reach the files. The default is ``5``.
    include_data : bool, optional
        Whether to include solution data when the product supports it. The
        default is ``True``.
    """

    directory: str | os.PathLike | None = None
    keep_last: int = 5
    include_data: bool = True

    def __post_init__(self):
        if self.keep_last < 1:
            raise ValueError(f"keep_last must be at least 1, got {self.keep_last}.")


@dataclass
class PoolConfig:
    """Warm standby sessions used for failover.

    Parameters
    ----------
    size : int, optional
        Total number of sessions: one active session plus ``size - 1`` warm
        standbys. The default is ``1`` (no standbys, no failover).
    launch_kwargs : dict, optional
        Keyword arguments for the product's launch function, used to start
        standbys. When omitted, standbys reuse the arguments that launched the
        active session if they are known.
    launcher : callable, optional
        Zero-argument callable that returns a new session. Takes precedence over
        ``launch_kwargs``.
    """

    size: int = 1
    launch_kwargs: dict[str, Any] | None = None
    launcher: Callable[[], Any] | None = None

    def __post_init__(self):
        if self.size < 1:
            raise ValueError(f"Pool size must be at least 1, got {self.size}.")


@dataclass
class ResilientConfig:
    """Configuration of resilient mode.

    Parameters
    ----------
    recovery : RecoveryPolicy or str, optional
        What to do when the server rejects a value. The default is
        ``RecoveryPolicy.WARN``.
    allow_model_activation : bool, optional
        Whether resilient mode may enable a governing model (for example the
        energy model) so that a write to an inactive setting succeeds. This changes
        the physics of the case, so it is disabled by default.
    activation_candidates : sequence of ActivationCandidate, optional
        Governing-model settings to try, before the product's built-in ones, when
        an inactive setting is written and ``allow_model_activation`` is
        ``True``. A candidate is kept only if it activates the setting; otherwise
        it is reverted. The default is no additional candidates.
    max_resolver_attempts : int, optional
        Maximum number of repair attempts for one write. The default is ``3``.
    clamp_tolerance : float, optional
        Largest overshoot that is clamped to the nearest bound, as a fraction of
        the allowed range (with a single bound, of that bound's magnitude). A
        value further outside the range is not repaired and the original error is
        raised. Use ``0`` to never clamp and ``math.inf`` to always clamp. The
        default is ``0.1``.
    auto_checkpoint : bool, optional
        Whether to write a checkpoint before each irreversible command (for
        example ``iterate`` or ``read_case``). The default is ``True``.
    auto_rollback : bool, optional
        Whether to restore that checkpoint when the irreversible command fails.
        The original error is raised afterwards in either case. The default is
        ``True``.
    journal_max_ops : int, optional
        Maximum number of operations kept in the journal. The default is
        ``10000``.
    checkpoint : CheckpointConfig, optional
        Checkpoint location and retention.
    pool : PoolConfig, optional
        Warm standby sessions for failover.
    """

    recovery: RecoveryPolicy | str = RecoveryPolicy.WARN
    allow_model_activation: bool = False
    activation_candidates: tuple[ActivationCandidate, ...] = ()
    max_resolver_attempts: int = 3
    clamp_tolerance: float = 0.1
    auto_checkpoint: bool = True
    auto_rollback: bool = True
    journal_max_ops: int = 10_000
    checkpoint: CheckpointConfig = field(default_factory=CheckpointConfig)
    pool: PoolConfig = field(default_factory=PoolConfig)

    def __post_init__(self):
        try:
            self.recovery = RecoveryPolicy(self.recovery)
        except ValueError as err:
            allowed = ", ".join(repr(p.value) for p in RecoveryPolicy)
            raise ValueError(
                f"Invalid recovery policy {self.recovery!r}; use one of {allowed}."
            ) from err
        self.activation_candidates = tuple(self.activation_candidates)
        for candidate in self.activation_candidates:
            if not isinstance(candidate, ActivationCandidate):
                raise TypeError(
                    "activation_candidates must contain ActivationCandidate "
                    f"objects, for example ActivationCandidate(path, value); got "
                    f"{candidate!r}."
                )
        if self.max_resolver_attempts < 0:
            raise ValueError("max_resolver_attempts must not be negative.")
        if not self.clamp_tolerance >= 0:
            raise ValueError(
                f"clamp_tolerance must be zero or positive, got {self.clamp_tolerance}."
            )
        if self.journal_max_ops < 1:
            raise ValueError("journal_max_ops must be at least 1.")
