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

"""Classify a caught exception into an actionable :class:`Classification`.

Fluent surfaces most errors to Python as ``RuntimeError(<fluent error text>)``
(the gRPC error interceptor flattens them), so text is often the only signal.
A handful of cases are typed (``InactiveObjectError``, ``ReadOnlyActionError``,
``DisallowedValuesError``) and a fatal server state is authoritative via the
shared ``ErrorState``. The classifier checks, in order:

1. **benign interrupt** -- ``RuntimeError("()")`` is Fluent's clean solver-stop
   sentinel, not an error;
2. **fatal** -- the session's ``ErrorState`` is ``"fatal"`` (or the server is no
   longer serving) -- catastrophic, triggers failover. This is the *only* source
   of a catastrophic classification; error text is never used to escalate to
   fatal, so a recoverable message that merely mentions "fatal" cannot trigger a
   failover;
3. **typed core errors** -- inactive target / read-only / disallowed value;
4. **text heuristics** -- "not active", "out of range", "allowed values", etc.;
5. **fallback** -- :attr:`ErrorCategory.UNKNOWN` (hard).
"""

from __future__ import annotations

from ansys.fluent.core.resilient import _compat
from ansys.fluent.core.resilient.types import (
    Classification,
    ErrorCategory,
    Severity,
)

#: The clean solver-stop / interrupt sentinel raised by interruptible commands.
_INTERRUPT_SENTINEL = "()"


def _import_core_errors():
    """Import the typed core exception classes, tolerating import failure.

    Returns a tuple ``(InactiveObjectError, ReadOnlyActionError,
    DisallowedValuesError, InvalidArgument)`` where any member may be ``None`` if
    it cannot be imported (keeps the classifier usable in isolation / tests).
    """
    try:
        from ansys.fluent.core.solver.flobject import (
            InactiveObjectError,
            ReadOnlyActionError,
        )
    except Exception:  # noqa: BLE001
        InactiveObjectError = ReadOnlyActionError = None
    try:
        from ansys.fluent.core.diagnostics.exceptions import (
            DisallowedValuesError,
            InvalidArgument,
        )
    except Exception:  # noqa: BLE001
        DisallowedValuesError = InvalidArgument = None
    return (
        InactiveObjectError,
        ReadOnlyActionError,
        DisallowedValuesError,
        InvalidArgument,
    )


_SEVERITY_BY_CATEGORY = {
    ErrorCategory.INACTIVE_TARGET: Severity.RECOVERABLE,
    ErrorCategory.OUT_OF_RANGE: Severity.RECOVERABLE,
    ErrorCategory.WRONG_VALUE: Severity.RECOVERABLE,
    ErrorCategory.WRONG_TYPE: Severity.RECOVERABLE,
    ErrorCategory.READ_ONLY: Severity.HARD,
    ErrorCategory.FATAL: Severity.CATASTROPHIC,
    ErrorCategory.BENIGN_INTERRUPT: Severity.BENIGN,
    ErrorCategory.UNKNOWN: Severity.HARD,
}


class ErrorClassifier:
    """Map a caught exception (and optional session) to a classification."""

    def __init__(self, adapter=None):
        if adapter is not None:
            classes = adapter.error_classes()
            self._inactive_err = classes.inactive
            self._read_only_err = classes.read_only
            self._disallowed_err = classes.disallowed
            self._invalid_arg_err = classes.invalid_arg
        else:
            (
                self._inactive_err,
                self._read_only_err,
                self._disallowed_err,
                self._invalid_arg_err,
            ) = _import_core_errors()

    @staticmethod
    def is_fatal(session) -> bool:
        """Authoritative check: is the server in a fatal state?"""
        return _compat.is_fatal(session)

    def classify(self, err: Exception, session=None, *, interruptible=False):
        """Classify ``err`` into a :class:`Classification`.

        ``session`` is optional; when given it is consulted for the authoritative
        fatal-state check (a fatal event poisons the whole session, so any error
        observed afterwards is really catastrophic).

        ``interruptible`` mirrors core PyFluent: the clean-stop sentinel
        ``RuntimeError("()")`` is only treated as a *benign* interrupt for an
        interruptible (solve) command -- exactly where core itself suppresses it.
        Anywhere else (e.g. a value ``set``) the same text is NOT swallowed; it is
        surfaced as a genuine error so behaviour is consistent, never
        inconsistently swallowed.
        """
        text = str(err)

        # 1. Clean solver stop / interrupt -- benign ONLY for interruptible
        #    (solve) commands, matching core's suppression. Elsewhere it is a real
        #    error and must be surfaced, not swallowed.
        if (
            interruptible
            and isinstance(err, RuntimeError)
            and text.strip() == _INTERRUPT_SENTINEL
        ):
            return self._make(
                ErrorCategory.BENIGN_INTERRUPT,
                "Solver was cleanly interrupted / stopped.",
            )

        # 2. Fatal server state is authoritative and poisons the session.
        if session is not None and _compat.is_fatal(session):
            return self._make(
                ErrorCategory.FATAL,
                "Fluent server is in a fatal error state; the session is "
                "unusable and requires failover.",
                details=_compat.fatal_details(session) or text,
            )

        # 3. Typed core errors.
        if self._inactive_err is not None and isinstance(err, self._inactive_err):
            return self._make(ErrorCategory.INACTIVE_TARGET, text)
        if self._read_only_err is not None and isinstance(err, self._read_only_err):
            return self._make(ErrorCategory.READ_ONLY, text)
        if self._disallowed_err is not None and isinstance(err, self._disallowed_err):
            return self._make(ErrorCategory.WRONG_VALUE, text)
        if self._invalid_arg_err is not None and isinstance(err, self._invalid_arg_err):
            return self._make(ErrorCategory.WRONG_VALUE, text)
        if isinstance(err, TypeError):
            return self._make(ErrorCategory.WRONG_TYPE, text)

        # 4. Text heuristics over the flattened Fluent error string.
        category = self._classify_text(text)
        return self._make(category, text)

    @staticmethod
    def _classify_text(text: str) -> ErrorCategory:
        # NOTE: this runs only when the authoritative fatal check (the shared
        # ``ErrorState``) already said the session is NOT fatal. We therefore do
        # *not* escalate to ``FATAL`` from text here: a recoverable or benign
        # message that merely mentions the word "fatal" (e.g. "may cause a fatal
        # error") must not trigger a failover. Catastrophic classification is
        # driven solely by the authoritative ``ErrorState`` in ``classify``.
        lowered = text.lower()
        if "not active" in lowered or "is not active" in lowered:
            return ErrorCategory.INACTIVE_TARGET
        if "read-only" in lowered or "read only" in lowered:
            return ErrorCategory.READ_ONLY
        if (
            "out of range" in lowered
            or "not in range" in lowered
            or "below minimum" in lowered
            or "above maximum" in lowered
            or "minimum" in lowered
            or "maximum" in lowered
            or "invalid parameter value" in lowered  # CFX phrasing
            or "out of bounds" in lowered
        ):
            return ErrorCategory.OUT_OF_RANGE
        if (
            "allowed value" in lowered
            or "not a valid" in lowered
            or "not allowed" in lowered
            or "disallowed" in lowered
        ):
            return ErrorCategory.WRONG_VALUE
        return ErrorCategory.UNKNOWN

    @staticmethod
    def _make(
        category: ErrorCategory, message: str, details: str | None = None
    ) -> Classification:
        return Classification(
            category=category,
            severity=_SEVERITY_BY_CATEGORY[category],
            message=message,
            details=details,
        )
