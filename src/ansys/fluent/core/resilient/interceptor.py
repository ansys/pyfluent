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

"""Transparent resilience for the settings service layer.

Every write and command on the typed settings tree -- whether the user writes
``solver.settings.setup.models.energy.enabled = True``, ``obj.set_state(v)``, or
``solver.settings.solution.run_calculation.iterate(iter_count=100)`` -- funnels
through two methods on the settings service object
(``ansys.fluent.core.services.settings.BaseSettings``):

* ``set_var(path, value)`` for every value write, and
* ``execute_cmd(path, command, **kwds)`` for every command.

:class:`ResilientSettingsService` wraps the live service and routes exactly those
two methods through the resilient envelope (classify -> auto-recover -> checkpoint
/ failover), while delegating every other method unchanged. Because the path is
already a string here, the existing classifier / resolver / checkpoint machinery
plugs straight in -- and the user's PyFluent code is completely unchanged.

The wrapper is deliberately transparent: it forwards all attribute access it does
not override to the wrapped service, so version-specific behaviour
(``is_wildcard`` and so on) keeps working.
"""

from __future__ import annotations

from ansys.fluent.core.resilient.checkpoint import is_irreversible
from ansys.fluent.core.resilient.errors import ErrorClassifier
from ansys.fluent.core.resilient.resolver import RecoverableErrorResolver
from ansys.fluent.core.resilient.types import StepOutcome


class ResilientSettingsService:
    """Resilience-enabled proxy over a live settings service.

    Parameters
    ----------
    inner :
        The real settings service (``BaseSettings`` subclass) to delegate to.
    controller :
        The :class:`~ansys.fluent.core.resilient.controller.ResilientController`
        that owns the session reference, checkpoint manager, pool, classifier and
        resolver. The service calls back into it for recovery, checkpointing and
        failover so all resilient state lives in one place.
    """

    def __init__(self, inner, controller):
        # Use object.__setattr__ to avoid the custom __getattr__ loop below.
        object.__setattr__(self, "_inner", inner)
        object.__setattr__(self, "_controller", controller)
        object.__setattr__(self, "_last_outcome", None)

    # -- the two intercepted methods -------------------------------------

    def set_var(self, path: str, value) -> None:
        """Set a value with transparent auto-recovery and failover."""
        outcome = self._controller.apply_set(self._inner, path, value)
        object.__setattr__(self, "_last_outcome", outcome)

    def execute_cmd(self, path: str, command: str, **kwds):
        """Execute a command, auto-checkpointing irreversible ones first."""
        full = f"{path}.{command}" if path else command
        if self._controller.auto_file_checkpoint and is_irreversible(full):
            self._controller.auto_checkpoint(full)
        outcome, result = self._controller.apply_command(
            self._inner, path, command, kwds
        )
        object.__setattr__(self, "_last_outcome", outcome)
        return result

    # -- transparent delegation ------------------------------------------

    def rebind_inner(self, inner) -> None:
        """Point the proxy at a new underlying service (after a failover)."""
        object.__setattr__(self, "_inner", inner)

    @property
    def inner(self):
        """The wrapped settings service."""
        return self._inner

    @property
    def last_outcome(self) -> StepOutcome | None:
        """The :class:`StepOutcome` of the most recent intercepted write."""
        return self._last_outcome

    def __getattr__(self, name):
        # Only reached for attributes not defined on this proxy; forward them to
        # the wrapped service so version-specific behaviour is preserved.
        return getattr(object.__getattribute__(self, "_inner"), name)

    def __setattr__(self, name, value):
        # Keep our own private attributes local; forward the rest to the inner
        # service so nothing it relies on is shadowed.
        if name in ("_inner", "_controller", "_last_outcome"):
            object.__setattr__(self, name, value)
        else:
            setattr(self._inner, name, value)


__all__ = ["ResilientSettingsService", "ErrorClassifier", "RecoverableErrorResolver"]
