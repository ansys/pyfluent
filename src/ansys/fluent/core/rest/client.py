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
import warnings

logger = logging.getLogger(__name__)

# HTTP status codes eligible for automatic retry.
_RETRYABLE_STATUS_CODES = frozenset({502, 503, 504})

# HTTP methods safe to retry automatically (idempotent).
_RETRYABLE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})


class FluentRestError(RuntimeError):
    """HTTP error returned by the Fluent REST server."""

    def __init__(self, status: int, message: str) -> None:
        self.status = status
        super().__init__(f"HTTP {status}: {message}")


class FluentRestClient:
    """HTTP client for the Fluent DataModel REST API.

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
        (``URLError``) or HTTP 502/503/504 responses.  Defaults to ``0``
        (no retries — fail immediately).
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
        max_retries: int = 0,
        retry_delay: float = 1.0,
        ssl_context: ssl.SSLContext | None = None,
    ) -> None:
        self._validate_base_url(base_url, auth_token, ssl_context)
        if timeout <= 0:
            raise ValueError("timeout must be > 0")
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        if retry_delay < 0:
            raise ValueError("retry_delay must be >= 0")
        self._base_url = base_url.rstrip("/")
        self._auth_token = auth_token
        self._component = component
        self._timeout = timeout
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._ssl_context = ssl_context
        self._api_base = f"api/{component}"
        self._is_closed = False

    @property
    def _is_secure(self) -> bool:
        """Return True if the connection is HTTPS, False otherwise."""
        return self._base_url.startswith("https://")

    # ------------------------------------------------------------------
    # Validation (SRP: input validation is a single, isolated concern)
    # ------------------------------------------------------------------

    @staticmethod
    def _validate_base_url(
        base_url: str,
        auth_token: str | None,
        ssl_context: ssl.SSLContext | None,
    ) -> None:
        """Validate *base_url* and warn on insecure auth transport.

        Raises
        ------
        ValueError
            If *base_url* has an unsupported scheme or no host.
        """
        parsed = urllib.parse.urlparse(base_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("scheme must be http or https")
        if not parsed.netloc:
            raise ValueError("base_url must include host")
        if auth_token and parsed.scheme == "http" and ssl_context is None:
            warnings.warn(
                "auth_token is being sent over plain HTTP. "
                "Use https:// to protect credentials in transit.",
                stacklevel=2,
            )

    # ------------------------------------------------------------------
    # HTTP transport internals
    # ------------------------------------------------------------------

    @staticmethod
    def _encode_path(path: str) -> str:
        """Percent-encode each segment of a slash-delimited path."""
        return "/".join(urllib.parse.quote(seg, safe="") for seg in path.split("/"))

    def _url(self, endpoint: str) -> str:
        """Build a full URL from *base_url* + *endpoint*."""
        return f"{self._base_url}/{endpoint}"

    def _build_auth_header(self) -> str | None:
        """Return the ``Authorization`` header value, or ``None``."""
        if not self._auth_token:
            return None
        return f"Bearer {hashlib.sha256(self._auth_token.encode()).hexdigest()}"

    def _build_request(
        self,
        method: str,
        url: str,
        body: Any = None,
    ) -> urllib.request.Request:
        """Assemble an :class:`urllib.request.Request`.

        Serialises *body* to JSON if provided and attaches auth headers.
        """
        data: bytes | None = None
        headers: dict[str, str] = {}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        auth = self._build_auth_header()
        if auth:
            headers["Authorization"] = auth
        return urllib.request.Request(
            url, data=data, headers=headers, method=method.upper()
        )

    @staticmethod
    def _parse_error_detail(exc: urllib.error.HTTPError) -> str:
        """Return a readable error message from an HTTP error response."""
        try:
            raw = exc.read().decode("utf-8", errors="replace")
            # Server returns plain text, not JSON
            if raw.strip():
                return raw.strip()
            return exc.reason
        except Exception:
            return exc.reason

    def _send_once(self, req: urllib.request.Request) -> Any:
        """Execute one HTTP request and decode JSON response content.

        Returns ``None`` for empty response bodies and ``{}`` for non-JSON
        non-empty bodies.
        """
        with urllib.request.urlopen(
            req, timeout=self._timeout, context=self._ssl_context
        ) as resp:  # nosec B310
            raw = resp.read()
            if not raw.strip():
                return None
            try:
                return json.loads(raw)
            except (json.JSONDecodeError, ValueError):
                return {}

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
        url = self._url(endpoint)
        req = self._build_request(method, url, body)

        retries = self._max_retries if method.upper() in _RETRYABLE_METHODS else 0
        for attempt in range(retries + 1):
            try:
                return self._send_once(req)
            except urllib.error.HTTPError as exc:
                detail = self._parse_error_detail(exc)
                if exc.code in _RETRYABLE_STATUS_CODES and attempt < retries:
                    time.sleep(self._retry_delay * (2**attempt))
                    continue
                raise FluentRestError(exc.code, detail) from exc
            except urllib.error.URLError as exc:
                if attempt < retries:
                    time.sleep(self._retry_delay * (2**attempt))
                    continue
                raise FluentRestError(0, str(exc.reason)) from exc
            except OSError as exc:
                # Catches RemoteDisconnected, ConnectionResetError,
                # ConnectionAbortedError — all signs the server died.
                raise FluentRestError(0, str(exc)) from exc

    # ------------------------------------------------------------------
    # Settings API — read / write
    # ------------------------------------------------------------------

    def get_static_info(self) -> dict[str, Any]:
        """Return the full settings schema (GET static-info)."""
        return self._request("GET", f"{self._api_base}/static-info")

    def get_var(self, path: str) -> Any:
        """Return the value at *path* (POST ``get_var``)."""
        return self._request(
            "POST", f"{self._api_base}/get_var", body={"path": path.lstrip("/")}
        )

    def set_var(self, path: str, value: Any) -> None:
        """Set the value at *path* (PUT {path})."""
        self._request("PUT", f"{self._api_base}/{self._encode_path(path)}", body=value)

    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return selected attributes for *path* (GET with ``attrs=...``).

        Raises
        ------
        FluentRestError
            If the request fails.
        """
        params = {"attrs": ",".join(attrs)}
        if recursive:
            params["recursive"] = "true"
        query = urllib.parse.urlencode(params)
        return self._request(
            "GET", f"{self._api_base}/{self._encode_path(path)}?{query}"
        )

    def get_object_names(self, path: str) -> list[str]:
        """Return child object names at *path* (GET {path}); return ``[]`` on 404.

        Raises
        ------
        FluentRestError
            If the request fails with a non-404 HTTP error.
        """
        try:
            result = self._request("GET", f"{self._api_base}/{self._encode_path(path)}")
        except FluentRestError as exc:
            if exc.status == 404:
                return []
            raise
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            # Real Fluent returns named objects as dict with names as keys:
            # {"hot-inlet": {...}, "cold-inlet": {...}}
            return list(result.keys())
        return []

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
        return self._request(
            "POST", f"{self._api_base}/{self._encode_path(path)}", body=body
        )

    def delete(self, path: str, name: str, *, ignore_not_found: bool = False) -> None:
        """Delete named object *name* at *path* (DELETE {path}/{name}).

        Raises
        ------
        FluentRestError
            If deletion fails, except when ``ignore_not_found=True`` and the
            server returns HTTP 404.
        """
        encoded_name = urllib.parse.quote(name, safe="")
        try:
            self._request(
                "DELETE", f"{self._api_base}/{self._encode_path(path)}/{encoded_name}"
            )
        except FluentRestError as exc:
            if ignore_not_found and exc.status == 404:
                return
            raise

    def rename(self, path: str, new: str, old: str) -> None:
        """Rename *old* to *new* at *path* (PUT {path}/{old})."""
        encoded_old = urllib.parse.quote(old, safe="")
        self._request(
            "PUT",
            f"{self._api_base}/{self._encode_path(path)}/{encoded_old}",
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

    def get_list_size(self, path: str) -> int:
        """Return element count at *path* (GET {path}); return 0 on 404.

        Raises
        ------
        FluentRestError
            If the request fails with a non-404 HTTP error.
        """
        try:
            result = self._request("GET", f"{self._api_base}/{self._encode_path(path)}")
        except FluentRestError as exc:
            if exc.status == 404:
                return 0
            raise
        if isinstance(result, list):
            return len(result)
        if isinstance(result, dict):
            # Explicit size field from list-objects
            if "size" in result:
                return result["size"]
            # Named-object containers: count the keys (object names)
            return len(result)
        return 0

    def resize_list_object(self, path: str, size: int) -> None:
        """Resize the list-object at *path* to *size* elements (POST {path})."""
        self._request(
            "POST",
            f"{self._api_base}/{self._encode_path(path)}",
            body={"new-size": size},
        )

    def _execute(self, path: str, name: str, **kwds) -> Any:
        """POST a command/query endpoint and return the raw response payload."""
        encoded_name = urllib.parse.quote(name, safe="")
        return self._request(
            "POST",
            f"{self._api_base}/{self._encode_path(path)}/{encoded_name}",
            body=kwds,
        )

    def execute_cmd(self, path: str, command: str, force: bool = True, **kwds) -> Any:
        """Execute *command* at *path*; appends ``force=true`` when requested."""
        encoded = urllib.parse.quote(command, safe="")
        endpoint = f"{self._api_base}/{self._encode_path(path)}/{encoded}"
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

        HTTP 403/409 are raised to the caller. Other failures are treated as
        shutdown-in-progress and suppressed.

        Raises
        ------
        FluentRestError
            If shutdown is blocked by the server (HTTP 403 or 409).
        """
        if self._is_closed:
            return
        try:
            self._request("POST", "api/app/exit")
        except FluentRestError as exc:
            if exc.status in (403, 409):
                logger.warning("Exit blocked (HTTP %d): %s", exc.status, exc)
                raise
            # Connection lost or other error → server already down
        except OSError:
            # Server died mid-response
            pass
        self._is_closed = True
        logger.info("Fluent server terminated.")

    def __enter__(self) -> "FluentRestClient":
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager — calls :meth:`exit`."""
        self.exit()
