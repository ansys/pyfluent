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

"""REST client for Fluent DataModel settings endpoints.

This client talks to ``/api/{component}/...`` and sends
``Authorization: Bearer <sha256(auth_token)>`` when a token is configured.
Most HTTP failures are raised as :class:`FluentRestError`.
"""

import hashlib
import json
import logging
import ssl
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)

_RETRYABLE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})

_RETRYABLE_STATUS_CODES = frozenset({502, 503, 504})


class FluentRestError(RuntimeError):
    """HTTP error raised when a Fluent REST request fails.

    This class is the **single place** that understands how to interpret
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
            message = body or exc.reason
            return cls(exc.code, message, retryable=exc.code in _RETRYABLE_STATUS_CODES)
        return cls(0, str(getattr(exc, "reason", exc)), retryable=True)


class FluentRestClient:
    """HTTP client for the Fluent DataModel REST API.

    This is typically obtained via :func:`ansys.fluent.core.rest.connect_to_webserver`
    rather than instantiated directly.

    Parameters
    ----------
    base_url : str
        Root URL of the Fluent REST server, e.g. ``"http://127.0.0.1:<port>"``.
        A trailing slash is stripped automatically.
    auth_token : str, optional
        Raw bearer token (the password set when Fluent was started).  Before
        each request the token is SHA-256 hashed and sent as
        ``Authorization: Bearer <sha256(auth_token)>``.
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"`` (solver).
        Use ``"fluent_meshing_1"`` for a meshing session.
    timeout : float, optional
        Socket timeout in seconds for every request.  Defaults to ``30.0``.
    max_retries : int, optional
        Maximum number of automatic retries on transient connection errors
        (``URLError``) or HTTP 502/503/504 responses.  Defaults to ``2``
        (retry up to 2 times with exponential backoff).
    retry_delay : float, optional
        Base delay in seconds between retries.  Uses exponential back-off:
        ``retry_delay * 2 ** attempt``.  Defaults to ``1.0``.
    ssl_context : ssl.SSLContext, optional
        Custom SSL context for HTTPS connections. Defaults to ``None``.
    """

    def __init__(
        self,
        base_url: str,
        *,
        auth_token: str | None = None,
        component: str = "fluent_1",
        timeout: float = 30.0,
        max_retries: int = 2,
        retry_delay: float = 1.0,
        ssl_context: ssl.SSLContext | None = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._auth_token = auth_token
        self._component = component
        self._timeout = timeout
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._ssl_context = ssl_context
        self._api_base = f"api/{component}"
        self._is_closed = False
        self._headers = self._make_auth_headers(auth_token)

    @staticmethod
    def _make_auth_headers(auth_token: str | None) -> dict[str, str]:
        """Return auth headers for *auth_token*, or empty dict if no token."""
        if not auth_token:
            return {}
        token_hash = hashlib.sha256(auth_token.encode()).hexdigest()
        return {"Authorization": f"Bearer {token_hash}"}

    # ------------------------------------------------------------------
    # HTTP transport internals
    # ------------------------------------------------------------------

    def _build_request(
        self,
        method: str,
        endpoint: str,
        body: Any = None,
    ) -> urllib.request.Request:
        """Assemble an :class:`urllib.request.Request`.

        Serialises *body* to JSON if provided and attaches auth headers.
        """
        url = f"{self._base_url}/{endpoint}"
        data: bytes | None = None
        headers: dict[str, str] = dict(self._headers)
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        return urllib.request.Request(
            url, data=data, headers=headers, method=method.upper()
        )

    def _send_once(self, req: urllib.request.Request) -> Any:
        """Execute one HTTP request and decode JSON response content.

        Returns ``None`` for empty response bodies and ``{}`` for non-JSON
        non-empty bodies.
        """
        with urllib.request.urlopen(
            req, timeout=self._timeout, context=self._ssl_context
        ) as resq:  # nosec B310
            raw = resq.read()
            if not raw.strip():
                return None
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {}

    def _send(self, req: urllib.request.Request) -> Any:
        """Send one request, translating transport errors to FluentRestError."""
        try:
            return self._send_once(req)
        except OSError as exc:
            raise FluentRestError.from_transport(exc) from exc

    def _back_off(self, attempt: int) -> None:
        """Sleep for an exponentially increasing amount of time."""
        time.sleep(self._retry_delay * (2**attempt))

    def _send_with_retry(self, req: urllib.request.Request, retries: int) -> Any:
        """Send a request with retry logic for retryable errors."""
        attempt = 0
        while True:
            try:
                return self._send(req)
            except FluentRestError as exc:
                if not exc.retryable or attempt >= retries:
                    raise
                self._back_off(attempt)
                attempt += 1

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        body: Any = None,
    ) -> Any:
        """Send an HTTP request with retry for idempotent methods only."""
        if self._is_closed:
            raise FluentRestError(0, "Session is closed")
        req = self._build_request(method, endpoint, body)
        retries = self._max_retries if method.upper() in _RETRYABLE_METHODS else 0
        return self._send_with_retry(req, retries)

    # ------------------------------------------------------------------
    # Settings API — read / write
    # ------------------------------------------------------------------

    def get_static_info(self, full: bool = False) -> dict[str, Any]:
        """Return the full settings schema (GET static-info)."""
        endpoint = f"{self._api_base}/static-info"
        if full:
            endpoint += "?full=true"
        return self._request("GET", endpoint)

    def get_var(self, path: str) -> Any:
        """Return the value at *path* (POST ``get_var``)."""
        return self._request(
            "POST", f"{self._api_base}/get_var", body={"path": path.lstrip("/")}
        )

    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return selected attributes for *path* (GET with ``attrs=...``)."""
        params = {"attrs": ",".join(attrs)}
        if recursive:
            params["recursive"] = "true"
        query = urllib.parse.urlencode(params)
        return self._request("GET", f"{self._api_base}/{path}?{query}")

    def get_object_names(self, path: str) -> list[str]:
        """Return child object names at *path* (GET {path}); return ``[]`` on 404.

        Raises
        ------
        FluentRestError
            If the request fails with a non-404 HTTP error.
        """
        result = self._request("GET", f"{self._api_base}/{path}")
        return self._names_from(result)

    def get_list_size(self, path: str) -> int:
        """Return element count at *path* (GET {path}); return 0 on 404.

        Raises
        ------
        FluentRestError
            If the request fails with a non-404 HTTP error.
        """
        result = self._request("GET", f"{self._api_base}/{path}")
        return self._size_from(result)

    def set_var(self, path: str, value: Any) -> None:
        """Write *value* at *path* (PUT ``{path}``)."""
        self._request("PUT", f"{self._api_base}/{path}", body=value)

    def resize_list_object(self, path: str, size: int) -> None:
        """Resize the list-object at *path* to *size* elements (POST ``{path}``)."""
        self._request("POST", f"{self._api_base}/{path}", body={"new-size": size})

    # ------------------------------------------------------------------
    # Settings API — named objects CRUD
    # ------------------------------------------------------------------

    def create(self, path: str, name: str = "", properties: dict | None = None) -> Any:
        """Create a child object at *path* (POST {path}).

        Raises
        ------
        FluentRestError
            If the request fails.
        """
        body = dict(properties) if properties else {}
        if name:
            body["name"] = name
        return self._request("POST", f"{self._api_base}/{path}", body=body)

    def delete(self, path: str, name: str, *, ignore_not_found: bool = False) -> None:
        """Delete named object *name* at *path* (DELETE {path}/{name}).

        Raises
        ------
        FluentRestError
            If deletion fails, except when ``ignore_not_found=True`` and the
            server returns HTTP 404.
        """
        try:
            endpoint = f"{self._api_base}/{path}/{urllib.parse.quote(name, safe='')}"
            self._request("DELETE", endpoint)
        except FluentRestError as exc:
            if not (ignore_not_found and exc.status == 404):
                raise

    def rename(self, path: str, new: str, old: str) -> None:
        """Rename *old* to *new* at *path* (PUT {path}/{old})."""
        encoded_old = urllib.parse.quote(old, safe="")
        self._request(
            "PUT",
            f"{self._api_base}/{path}/{encoded_old}",
            body={"name": new},
        )

    def delete_child_objects(
        self,
        path: str,
        obj_type: str,
        child_names: list[str],
    ) -> None:
        """Delete specific named children of *obj_type* under *path*."""
        for name in child_names:
            self.delete(f"{path}/{obj_type}", name)

    def delete_all_child_objects(self, path: str, obj_type: str) -> None:
        """Delete all named children of *obj_type* under *path*."""
        names = self.get_object_names(f"{path}/{obj_type}")
        self.delete_child_objects(path, obj_type, names)

    def _execute(self, path: str, name: str, **kwds) -> Any:
        """POST a command/query endpoint and return the raw response payload."""
        endpoint = f"{self._api_base}/{path}/{urllib.parse.quote(name, safe='')}"
        return self._request("POST", endpoint, body=kwds)

    def execute_cmd(self, path: str, command: str, force: bool = True, **kwds) -> Any:
        """Execute *command* at *path*; appends ``force=true`` when requested."""
        endpoint = f"{self._api_base}/{path}/{urllib.parse.quote(command, safe='')}"
        if force:
            endpoint += "?force=true"
        return self._request("POST", endpoint, body=kwds)

    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute *query* at *path* (POST {path}/{query})."""
        return self._execute(path, query, **kwds)

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------

    def exit(self) -> None:
        """Request shutdown via ``POST /api/app/exit`` and mark session closed.

        Idempotent — safe to call multiple times. HTTP 403/409 are raised
        to the caller. Other failures are treated as shutdown-in-progress and suppressed.

        Raises
        ------
        FluentRestError
            If shutdown is blocked by the server (HTTP 403 or 409).
        """
        if self._is_closed:
            return  # Already closed; this call is idempotent
        self._request("POST", "api/app/exit")
        self._is_closed = True
        logger.info("Fluent server terminated.")

    def __enter__(self) -> "FluentRestClient":
        """Enter the context manager."""
        return self

    def __exit__(
        self,
        exc_type: object | None,
        exc_value: object | None,
        traceback: object | None,
    ) -> None:
        """Exit the context manager — calls :meth:`exit`."""
        self.exit()

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------

    @staticmethod
    def _names_from(result: Any) -> list[str]:
        """Normalise a child-listing response to a plain list of names.

        The server returns either a JSON array ``["a", "b"]`` or a dict
        keyed by object name ``{"a": {...}, "b": {...}}``.
        """
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            return list(result.keys())
        return []

    @staticmethod
    def _size_from(result: Any) -> int:
        """Extract an element count from a list-object response.

        A list-object reports its length directly; a named-object container
        may include an explicit ``size`` field or just its key count.
        """
        if isinstance(result, list):
            return len(result)
        if isinstance(result, dict):
            return result.get("size", len(result))
        return 0
