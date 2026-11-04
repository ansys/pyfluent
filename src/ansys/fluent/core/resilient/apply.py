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

"""Apply a single set / command with classification and auto-recovery.

:class:`SafeApplier` is the heart of the per-step resilience envelope:

* **set** captures the old value (for rollback), refuses to write an *inactive*
  target before it reaches Fluent (a raw inactive set can crash the solver),
  then classifies any failure -- benign interrupts succeed, catastrophic errors
  propagate (the pool fails over), recoverable errors go to the resolver, and
  hard errors raise :class:`UnrecoverableStepError`;
* **command** runs through the same envelope; a clean solver stop
  (``RuntimeError("()")``) is treated as success.
"""

from __future__ import annotations

from ansys.fluent.core.resilient import _compat
from ansys.fluent.core.resilient.errors import ErrorClassifier
from ansys.fluent.core.resilient.exceptions import UnrecoverableStepError
from ansys.fluent.core.resilient.resolver import RecoverableErrorResolver
from ansys.fluent.core.resilient.types import (
    Classification,
    ErrorCategory,
    Severity,
    StepOutcome,
)


def _brief(value) -> object:
    if isinstance(value, (str, int, float, bool, type(None))):
        return value
    if isinstance(value, dict):
        return f"<dict:{len(value)} keys>"
    if isinstance(value, (list, tuple)):
        return f"<{type(value).__name__}:{len(value)}>"
    return repr(value)


class SafeApplier:
    """Apply individual mutations against one live session, resiliently."""

    def __init__(
        self,
        session,
        *,
        classifier: ErrorClassifier | None = None,
        resolver: RecoverableErrorResolver | None = None,
        max_resolver_attempts: int = 3,
    ):
        self.session = session
        self.classifier = classifier or ErrorClassifier()
        self.resolver = resolver or RecoverableErrorResolver(
            session, max_attempts=max_resolver_attempts
        )

    def rebind(self, session) -> None:
        """Point the applier at a new session (after a failover)."""
        self.session = session
        self.resolver.session = session

    # -- set --------------------------------------------------------------

    def set(self, path: str, value, *, _recover: bool = True) -> StepOutcome:
        """Apply ``obj.set_state(value)`` at ``path`` with resilience.

        When ``_recover`` is ``False`` the raw error is raised instead of being
        routed to the resolver (used internally by the resolver's retry loop to
        avoid unbounded recursion).

        Raises
        ------
        Exception
            Re-raises a catastrophic (fatal) error so the caller can fail over,
            and the raw error when ``_recover`` is ``False``.
        UnrecoverableStepError
            If the target is inactive or the error is hard / unresolvable.
        """
        obj = _compat.resolve(self.session, path)
        inactive_outcome = self._handle_inactive(obj, path, value, _recover)
        if inactive_outcome is not None:
            return inactive_outcome
        old_value = None
        try:
            old_value = obj.get_state()
        except Exception:  # noqa: BLE001
            old_value = None
        try:
            obj.set_state(value)
        except Exception as err:  # noqa: BLE001
            if not _recover:
                raise
            return self._handle_set_failure(path, value, old_value, err)
        return StepOutcome(
            path=path,
            ok=True,
            old_value=_brief(old_value),
            new_value=_brief(value),
        )

    def _handle_inactive(self, obj, path: str, value, recover: bool):
        """Handle an inactive target before attempting a (crash-prone) set.

        Setting an inactive object can crash the solver, so we never write to one
        directly. When recovery is enabled we first try to *activate* it (the
        resolver discovers, by live introspection, which governing model turns it
        on) and retry; only if that fails do we refuse with a clear error.

        Returns a :class:`StepOutcome` if the target was inactive (recovered or
        raised), or ``None`` if the target is active and the normal path should
        proceed.
        """
        is_active = getattr(obj, "is_active", None)
        if not callable(is_active):
            return None
        try:
            active = bool(is_active())
        except Exception:  # noqa: BLE001
            active = False
        if active:
            return None
        if recover:
            cls = Classification(
                category=ErrorCategory.INACTIVE_TARGET,
                severity=Severity.RECOVERABLE,
                message=(f"{path!r} is inactive in the current model state."),
            )
            try:
                return self.resolver.resolve_and_retry(path, value, self, cls)
            except UnrecoverableStepError:
                raise
        raise UnrecoverableStepError(
            f"{path!r} is inactive in the current model state; enable the "
            "governing model / assign the zone type first."
        )

    def _handle_set_failure(
        self, path: str, value, old_value, err: Exception
    ) -> StepOutcome:
        # A set is not interruptible, so the clean-stop sentinel is surfaced as a
        # real error here (consistent handling; never swallowed).
        cls = self.classifier.classify(err, self.session, interruptible=False)
        if cls.catastrophic:
            raise err
        if cls.recoverable:
            outcome = self.resolver.resolve_and_retry(path, value, self, cls)
            if outcome.old_value is None:
                outcome.old_value = _brief(old_value)
            return outcome
        raise UnrecoverableStepError(
            f"Could not apply {path!r}: {cls.message}"
        ) from err

    # -- command ----------------------------------------------------------

    def command(self, path: str, **kwargs) -> StepOutcome:
        """Invoke a settings command at ``path`` with resilience.

        A clean solver stop (``RuntimeError("()")``) is treated as success; a
        catastrophic error propagates so the caller can fail over.

        Raises
        ------
        Exception
            Re-raises a catastrophic (fatal) error so the caller can fail over.
        UnrecoverableStepError
            If the path is not a callable command or the command fails with a
            non-catastrophic, non-benign error.
        """
        parent, leaf = _compat.resolve_parent(self.session, path)
        method = getattr(parent, leaf, None)
        if not callable(method):
            raise UnrecoverableStepError(
                f"{path!r} does not resolve to a callable command."
            )
        try:
            result = method(**kwargs) if kwargs else method()
        except Exception as err:  # noqa: BLE001
            from ansys.fluent.core.resilient.controller import (
                _is_interruptible_command,
            )

            cls = self.classifier.classify(
                err, self.session, interruptible=_is_interruptible_command(path)
            )
            if cls.severity.value == "benign":
                return StepOutcome(path=path, ok=True, result="interrupted")
            if cls.catastrophic:
                raise
            raise UnrecoverableStepError(
                f"Command {path!r} failed: {cls.message}"
            ) from err
        return StepOutcome(path=path, ok=True, result=_brief(result))
