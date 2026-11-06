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

"""Backend-neutral transport contract for the platform layer.

A transport owns the live link to a solver server: it carries request
metadata/authentication, reports readiness and error state, and can be opened
and closed. Concrete transports (for example gRPC or REST) implement this
contract; higher layers depend only on the protocol so the communication
backend can be swapped without touching them.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable


@runtime_checkable
class ErrorState(Protocol):
    """Latched error condition shared across a transport's services.

    Once set, services can inspect it to fail fast instead of issuing further
    calls over a broken connection.
    """

    @property
    def name(self) -> str:
        """Current error name, or an empty value when no error is set."""
        ...

    @property
    def details(self) -> str:
        """Human-readable details for the current error."""
        ...

    def set(self, name: str, details: str) -> None:
        """Latch an error condition."""
        ...

    def clear(self) -> None:
        """Clear any latched error condition."""
        ...


@runtime_checkable
class Transport(Protocol):
    """Backend-neutral connection to a solver server.

    This is the boundary the rest of the platform depends on. Implementations
    encapsulate everything backend-specific (channel setup, interceptors,
    protocol negotiation) behind these members.
    """

    @property
    def metadata(self) -> Sequence[tuple[str, str]]:
        """Per-request metadata/authentication headers."""
        ...

    @property
    def error_state(self) -> ErrorState:
        """Shared error state for this transport's services."""
        ...

    @property
    def is_serving(self) -> bool:
        """Whether the server is reachable and ready to serve requests."""
        ...

    def connect(self) -> None:
        """Open the connection, making the transport ready for use."""
        ...

    def close(self) -> None:
        """Close the connection and release its resources."""
        ...
