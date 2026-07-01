# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
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

"""REST error types for the Fluent REST client."""

import urllib.error

# Lives here because FluentRestError.from_transport is its only consumer.
_RETRYABLE_STATUS_CODES = frozenset({502, 503, 504})


class FluentRestError(RuntimeError):
    """HTTP error raised when a Fluent REST request fails.

    This class is the single place that understands how to interpret
    transport-level failures.  It knows which HTTP status codes come from
    the server vs. which originate from a broken connection, and it knows
    which failures are transient enough to be worth retrying.

    Attributes
    ----------
    status : int
        HTTP status code.  ``0`` means the request never reached the
        server (connection refused, reset, DNS failure, etc.).
    retryable : bool
        ``True`` when the failure is transient — a 502/503/504 gateway
        error or a connection-level ``OSError`` — and re-issuing the
        same request has a reasonable chance of succeeding.
    """

    def __init__(self, status: int, message: str, *, retryable: bool = False) -> None:
        self.status = status
        self.retryable = retryable
        super().__init__(f"HTTP {status}: {message}")

    # ------------------------------------------------------------------
    # Named factories — callers never hard-code status codes or strings
    # ------------------------------------------------------------------

    @classmethod
    def from_transport(cls, exc: OSError) -> "FluentRestError":
        """Construct from a stdlib transport exception.

        ``urllib`` raises ``HTTPError`` (a subclass of ``OSError``) when
        the server replies with an error status, and plain ``OSError``
        when the connection itself fails.  This factory inspects the
        exception once and produces a fully-populated domain error.
        """
        if isinstance(exc, urllib.error.HTTPError):
            body = exc.read().decode("utf-8", errors="replace").strip()
            return cls(
                exc.code,
                body or exc.reason,
                retryable=exc.code in _RETRYABLE_STATUS_CODES,
            )
        return cls(0, str(getattr(exc, "reason", exc)), retryable=True)

    @classmethod
    def not_found(cls, resource: str) -> "FluentRestError":
        """Construct a 404 Not Found error."""
        return cls(404, f"Not found: {resource}")
