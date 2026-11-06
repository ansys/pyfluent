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

"""Resilient mode for Fluent solver sessions.

Enable it with ``resilient_mode=True`` on any launch or connect function, or with
:func:`enable_resilient_mode` on an existing solver session. Ordinary PyFluent
code then gains:

* repair of rejected values (clamp, closest allowed value, numeric conversion),
  governed by :class:`RecoveryPolicy`;
* optional activation of the governing model of an inactive setting;
* a journal of settings writes with undo and redo;
* checkpoints (case and data files), written automatically before irreversible
  commands, with automatic rollback when such a command fails; and
* optional failover to warm standby sessions.

The behavior is implemented by the product-agnostic engine in
:mod:`ansys.fluent.core.resilient.engine`; :class:`FluentAdapter` supplies the
Fluent-specific parts.

Examples
--------
>>> import ansys.fluent.core as pyfluent
>>> solver = pyfluent.launch_fluent(mode="solver", resilient_mode=True)
>>> solver.settings.file.read_case(file_name="mixing_elbow.cas.h5")
>>> solver.resilient.checkpoint("configured")
>>> solver.settings.solution.run_calculation.iterate(iter_count=100)
>>> solver.resilient.rollback("configured")
"""

from __future__ import annotations

from typing import Any
import warnings

from ansys.fluent.core.resilient.engine import (
    ActivationCandidate,
    Checkpoint,
    CheckpointConfig,
    CheckpointError,
    Classification,
    CommandOp,
    ErrorCategory,
    ErrorClasses,
    EventKind,
    FailoverError,
    Fix,
    Journal,
    ObjectOp,
    PathResolutionError,
    PoolConfig,
    RecoveryPolicy,
    ResilientAdapter,
    ResilientConfig,
    ResilientController,
    ResilientError,
    ResilientEvent,
    ResilientFailoverWarning,
    ResilientRecoveryWarning,
    ResilientSession,
    ResilientWarning,
    SetOp,
    Severity,
    StepOutcome,
    WarmSessionPool,
    disable_resilient_mode,
)
from ansys.fluent.core.resilient.engine import (
    enable_resilient_mode as _enable_resilient_mode,
)
from ansys.fluent.core.resilient.engine import is_resilient
from ansys.fluent.core.resilient.fluent_adapter import FluentAdapter


def _unsupported_session_message(session: Any) -> str | None:
    """Return why resilient mode cannot apply to ``session``, or ``None``."""
    from ansys.fluent.core.solver.session.solver import Solver

    if isinstance(session, Solver):
        return None
    return (
        "resilient mode applies to gRPC solver sessions only, not to "
        f"{type(session).__name__}."
    )


def enable_resilient_mode(
    session: Any,
    config: ResilientConfig | None = None,
    *,
    pool_size: int | None = None,
) -> Any:
    """Enable resilient mode on a live Fluent solver session.

    Parameters
    ----------
    session : Solver
        A live solver session.
    config : ResilientConfig, optional
        Resilient-mode configuration. The default configuration is used when
        omitted.
    pool_size : int, optional
        Shortcut for ``config.pool.size``. A value greater than ``1`` launches warm
        standby sessions for failover.

    Returns
    -------
    Solver
        The same session, with resilient controls available as
        ``session.resilient``.

    Raises
    ------
    ResilientError
        If the session is not a solver session, resilient mode is already
        enabled, or standby sessions cannot be launched.
    """
    reason = _unsupported_session_message(session)
    if reason is not None:
        raise ResilientError(f"Cannot enable resilient mode: {reason}")
    return _enable_resilient_mode(
        session, config, adapter=FluentAdapter(), pool_size=pool_size
    )


def _enable_on_new_session(
    session: Any, config: ResilientConfig | None, *, launched: bool
) -> Any:
    """Apply ``resilient_mode=True`` passed to a launch or connect function.

    ``launched`` is ``True`` for a session started by the call, whose journal then
    covers its whole history.
    """
    from ansys.fluent.core.diagnostics.exceptions import PyFluentUserWarning

    reason = _unsupported_session_message(session)
    if reason is not None:
        warnings.warn(
            f"resilient_mode=True was ignored: {reason}",
            PyFluentUserWarning,
            stacklevel=3,
        )
        return session
    return _enable_resilient_mode(
        session, config, adapter=FluentAdapter(), journal_complete=launched
    )


__all__ = [
    "ActivationCandidate",
    "Checkpoint",
    "CheckpointConfig",
    "CheckpointError",
    "Classification",
    "CommandOp",
    "ErrorCategory",
    "ErrorClasses",
    "EventKind",
    "FailoverError",
    "Fix",
    "FluentAdapter",
    "Journal",
    "ObjectOp",
    "PathResolutionError",
    "PoolConfig",
    "RecoveryPolicy",
    "ResilientAdapter",
    "ResilientConfig",
    "ResilientController",
    "ResilientError",
    "ResilientEvent",
    "ResilientFailoverWarning",
    "ResilientRecoveryWarning",
    "ResilientSession",
    "ResilientWarning",
    "SetOp",
    "Severity",
    "StepOutcome",
    "WarmSessionPool",
    "disable_resilient_mode",
    "enable_resilient_mode",
    "is_resilient",
]
