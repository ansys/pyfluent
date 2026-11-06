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

"""Classify exceptions raised by settings calls.

The order of checks is:

1. the clean-stop sentinel ``RuntimeError("()")`` of an interruptible command is
   benign;
2. a fatal error reported by the product is catastrophic;
3. typed product exceptions (inactive, read-only, disallowed value);
4. message heuristics for errors the server reports as plain text;
5. an otherwise unknown error is catastrophic only if the server no longer
   answers a health check.

Error text alone never makes an error catastrophic, so a message that merely
mentions "fatal" cannot trigger a failover.
"""

from __future__ import annotations

from typing import Any

from .adapter import ResilientAdapter
from .types import Classification, ErrorCategory, Severity

#: Clean-stop sentinel raised by an interrupted solve command.
_INTERRUPT_SENTINEL = "()"

_SEVERITY = {
    ErrorCategory.INACTIVE_TARGET: Severity.RECOVERABLE,
    ErrorCategory.OUT_OF_RANGE: Severity.RECOVERABLE,
    ErrorCategory.WRONG_VALUE: Severity.RECOVERABLE,
    ErrorCategory.WRONG_TYPE: Severity.RECOVERABLE,
    ErrorCategory.READ_ONLY: Severity.HARD,
    ErrorCategory.FATAL: Severity.CATASTROPHIC,
    ErrorCategory.BENIGN_INTERRUPT: Severity.BENIGN,
    ErrorCategory.UNKNOWN: Severity.HARD,
}

_TEXT_RULES: tuple[tuple[ErrorCategory, tuple[str, ...]], ...] = (
    (
        ErrorCategory.INACTIVE_TARGET,
        ("not active", "is inactive", "currently inactive"),
    ),
    (ErrorCategory.READ_ONLY, ("read-only", "read only")),
    (
        ErrorCategory.OUT_OF_RANGE,
        (
            "out of range",
            "not in range",
            "below minimum",
            "above maximum",
            "out of bounds",
            "invalid parameter value",
        ),
    ),
    (
        ErrorCategory.WRONG_VALUE,
        ("allowed value", "not a valid", "not allowed", "disallowed"),
    ),
)


def make_classification(
    category: ErrorCategory, message: str, details: str | None = None
) -> Classification:
    """Build a classification with the default severity of ``category``."""
    return Classification(
        category=category,
        severity=_SEVERITY[category],
        message=message,
        details=details,
    )


class ErrorClassifier:
    """Map an exception, and optionally its session, to a :class:`Classification`."""

    def __init__(self, adapter: ResilientAdapter):
        self._adapter = adapter
        self._classes = adapter.error_classes()

    def classify(
        self, err: BaseException, session: Any = None, *, interruptible: bool = False
    ) -> Classification:
        """Classify ``err``.

        Parameters
        ----------
        err : BaseException
            The exception to classify.
        session : optional
            The session the error came from. When given, the product's fatal state
            and the server health are consulted.
        interruptible : bool, optional
            Whether the failing call was an interruptible (solve) command.

        Returns
        -------
        Classification
            The classification of ``err``.
        """
        text = str(err)
        if (
            interruptible
            and isinstance(err, RuntimeError)
            and text.strip() == _INTERRUPT_SENTINEL
        ):
            return make_classification(
                ErrorCategory.BENIGN_INTERRUPT, "The command was interrupted."
            )

        if session is not None and self._adapter.is_fatal(session):
            return make_classification(
                ErrorCategory.FATAL,
                f"The {self._adapter.product_name} server reported a fatal error.",
                details=self._adapter.fatal_details(session) or text,
            )

        category = self._typed_category(err)
        if category is None:
            category = self._text_category(text)
        if (
            category is ErrorCategory.UNKNOWN
            and session is not None
            and not self._adapter.is_server_healthy(session)
        ):
            return make_classification(
                ErrorCategory.FATAL,
                f"The {self._adapter.product_name} server is no longer serving.",
                details=text,
            )
        return make_classification(category, text)

    def _typed_category(self, err: BaseException) -> ErrorCategory | None:
        classes = self._classes
        for cls, category in (
            (classes.inactive, ErrorCategory.INACTIVE_TARGET),
            (classes.read_only, ErrorCategory.READ_ONLY),
            (classes.disallowed, ErrorCategory.WRONG_VALUE),
            (classes.invalid_arg, ErrorCategory.WRONG_VALUE),
        ):
            if cls is not None and isinstance(err, cls):
                return category
        if isinstance(err, TypeError):
            return ErrorCategory.WRONG_TYPE
        return None

    @staticmethod
    def _text_category(text: str) -> ErrorCategory:
        lowered = text.lower()
        for category, needles in _TEXT_RULES:
            if any(needle in lowered for needle in needles):
                return category
        return ErrorCategory.UNKNOWN
