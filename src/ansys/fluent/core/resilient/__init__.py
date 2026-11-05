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

"""Resilient execution runtime for PyFluent.

A native, transport-agnostic layer that makes solver workflows survivable:

* **checkpoint / undo / redo** across two tiers -- in-memory settings snapshots
  for reversible changes and case/data file checkpoints for irreversible
  commands, unified under a single undo/redo stack;
* **automatic recovery** from non-catastrophic Fluent errors, using live object
  introspection (``is_active`` / ``allowed_values`` / ``min`` / ``max``) plus
  static error classification to repair and retry;
* **warm-pool failover** -- a configurable pool of live sessions; on a fatal
  error the runtime promotes a standby and replays the last good checkpoint.

This package depends on neither ``fastmcp`` nor ``ansys.fluent.core.ai``; it is a
core capability usable directly by humans or by agentic hosts.

Example
-------
>>> import ansys.fluent.core as pyfluent
>>> from ansys.fluent.core.resilient import ResilientSolver
>>> session = pyfluent.launch_fluent(mode="solver")
>>> with ResilientSolver(session, pool_size=3) as rsolver:
...     rsolver.command("file.read_case_data", file_name="elbow.cas.h5")
...     rsolver.set("setup.models.energy.enabled", True)
...     rsolver.checkpoint("pre-iterate")
...     rsolver.command("solution.run_calculation.iterate", iter_count=100)
"""

from ansys.fluent.core.resilient.adapter import (
    DEFAULT_ADAPTER,
    ErrorClasses,
    ResilientAdapter,
    adapter_for,
)
from ansys.fluent.core.resilient.apply import SafeApplier
from ansys.fluent.core.resilient.attach import (
    enable_resilient_mode,
    is_resilient,
    last_outcome,
    on_journal_event,
)
from ansys.fluent.core.resilient.checkpoint import (
    CheckpointManager,
    is_irreversible,
)
from ansys.fluent.core.resilient.controller import ResilientController
from ansys.fluent.core.resilient.errors import ErrorClassifier
from ansys.fluent.core.resilient.exceptions import (
    CheckpointError,
    FailoverError,
    PathResolutionError,
    ResilientError,
    UnrecoverableStepError,
)
from ansys.fluent.core.resilient.filecheck import (
    FileCheckpointConfig,
    FileCheckpointStore,
)
from ansys.fluent.core.resilient.fluent_adapter import FluentAdapter
from ansys.fluent.core.resilient.health import SessionHealthMonitor
from ansys.fluent.core.resilient.journal import CommandOp, Journal, SetOp
from ansys.fluent.core.resilient.pool import PoolConfig, WarmSessionPool
from ansys.fluent.core.resilient.resolver import RecoverableErrorResolver
from ansys.fluent.core.resilient.solver import ResilientConfig, ResilientSolver
from ansys.fluent.core.resilient.types import (
    CheckpointKind,
    Classification,
    ErrorCategory,
    Fix,
    Severity,
    StepOutcome,
    UndoEntry,
)

__all__ = [
    # transparent resilient mode (primary entry points)
    "enable_resilient_mode",
    "is_resilient",
    "last_outcome",
    "on_journal_event",
    "ResilientController",
    "Journal",
    "SetOp",
    "CommandOp",
    # the reusable-framework seam (product adapters)
    "ResilientAdapter",
    "ErrorClasses",
    "FluentAdapter",
    "DEFAULT_ADAPTER",
    "adapter_for",
    # explicit facade (advanced)
    "ResilientSolver",
    "ResilientConfig",
    "PoolConfig",
    "WarmSessionPool",
    "FileCheckpointConfig",
    "FileCheckpointStore",
    "CheckpointManager",
    "SessionHealthMonitor",
    "SafeApplier",
    "ErrorClassifier",
    "RecoverableErrorResolver",
    "is_irreversible",
    # types
    "Classification",
    "CheckpointKind",
    "ErrorCategory",
    "Fix",
    "Severity",
    "StepOutcome",
    "UndoEntry",
    # exceptions
    "ResilientError",
    "PathResolutionError",
    "UnrecoverableStepError",
    "FailoverError",
    "CheckpointError",
]
