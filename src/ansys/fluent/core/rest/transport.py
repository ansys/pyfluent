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

"""HTTP transport strategy for the Fluent REST client.

Defines the :class:`RequestStrategy` protocol and the real
:class:`HttpRequestStrategy` implementation.  Inject a fake strategy
in unit tests — no subclassing needed (structural subtyping via Protocol).
"""

import hashlib
import json
import ssl
import time
from typing import Any, Protocol, runtime_checkable

import urllib.request

from ansys.fluent.core.rest.errors import FluentRestError

# Only idempotent methods are retried on transient failures.
_RETRYABLE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})


@runtime_checkable
class RequestStrategy(Protocol):
    """Protocol satisfied by any object that can execute an HTTP request.

    Both the real :class:`HttpRequestStrategy` and any test double satisfy
    this protocol structurally — no inheritance required.
    """

    def request(self, method: str, endpoint: str, *, body: Any = None) -> Any:
        """Execute one HTTP request and return the decoded JSON response.

        Parameters
        ----------
        method : str
            HTTP verb (``"GET"``, ``"POST"``, ``"PUT"``, ``"DELETE"``).
        endpoint : str
            API path relative to the server root, e.g.
            ``"api/fluent_1/get_var"``.
        body : Any, optional
            Request payload; serialised to JSON before sending.

        Returns
        -------
        Any
            Decoded JSON body, ``None`` for empty responses, or ``{}`` for
            non-JSON bodies.

        Raises
        ------
        FluentRestError
            On any HTTP or transport failure.
        """
        ...  # pragma: no cover


def _make_auth_headers(auth_token: str | None) -> dict[str, str]:
    """Return ``Authorization`` header dict, or ``{}`` when there is no token."""
    if not auth_token:
        return {}
    token_hash = hashlib.sha256(auth_token.encode()).hexdigest()
    return {"Authorization": f"Bearer {token_hash}"}


class HttpRequestStrategy:
    """Real HTTP transport built on stdlib ``urllib``.

    Parameters
    ----------
    base_url : str
        Root URL of the Fluent REST server, e.g. ``"http://127.0.0.1:5000"``.
        A trailing slash is stripped automatically.
    auth_token : str, optional
        Raw bearer token; SHA-256 hashed before transmission.
    timeout : float, optional
        Socket timeout in seconds. Defaults to ``30.0``.
    max_retries : int, optional
        Maximum automatic retries on transient errors. Defaults to ``2``.
    retry_delay : float, optional
        Base delay between retries (exponential back-off). Defaults to ``1.0``.
    ssl_context : ssl.SSLContext, optional
        Custom SSL context for HTTPS connections.
    """

    def __init__(
        self,
        base_url: str,
        *,
        auth_token: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 2,
        retry_delay: float = 1.0,
        ssl_context: ssl.SSLContext | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._ssl_context = ssl_context
        self._headers = _make_auth_headers(auth_token)

    # ------------------------------------------------------------------
    # Internal plumbing
    # ------------------------------------------------------------------

    def _build_request(
        self,
        method: str,
        url: str,
        body: Any = None,
    ) -> urllib.request.Request:
        data: bytes | None = None
        headers: dict[str, str] = dict(self._headers)
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        return urllib.request.Request(
            url, data=data, headers=headers, method=method.upper()
        )

    def _send_once(self, req: urllib.request.Request) -> Any:
        with urllib.request.urlopen(  # nosec B310
            req, timeout=self._timeout, context=self._ssl_context
        ) as resp:
            raw = resp.read()
            if not raw.strip():
                return None
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {}

    def _send(self, req: urllib.request.Request) -> Any:
        try:
            return self._send_once(req)
        except OSError as exc:
            raise FluentRestError.from_transport(exc) from exc

    def _back_off(self, attempt: int) -> None:
        time.sleep(self._retry_delay * (2**attempt))

    def _send_with_retry(self, req: urllib.request.Request, retries: int) -> Any:
        attempt = 0
        while True:
            try:
                return self._send(req)
            except FluentRestError as exc:
                if not exc.retryable or attempt >= retries:
                    raise
                self._back_off(attempt)
                attempt += 1

    # ------------------------------------------------------------------
    # RequestStrategy implementation
    # ------------------------------------------------------------------

    def request(self, method: str, endpoint: str, *, body: Any = None) -> Any:
        """Implement :class:`RequestStrategy` — build, send, and retry."""
        url = f"{self._base_url}/{endpoint}"
        req = self._build_request(method, url, body)
        retries = self._max_retries if method.upper() in _RETRYABLE_METHODS else 0
        return self._send_with_retry(req, retries)
