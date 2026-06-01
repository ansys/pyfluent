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

"""Pure-Python REST client for the Fluent solver settings (DataModel API).

Connects to the Fluent embedded web server that exposes the solver settings
via a DataModel REST API.  The base path for all settings endpoints is
``/api/{component}/`` where *component* is ``"fluent_1"`` for a solver session
(``"fluent_meshing_1"`` for a meshing session).

API endpoints (from ``/openapi.json`` on a live Fluent server)
--------------------------------------------------------------

.. code-block:: text

    GET  /api/fluent_1/static-info
         Returns the full settings schema.

    POST /api/fluent_1/get_var
         body: { "path": "<path>" }
         Returns the current value at <path>.

    GET  /api/fluent_1/{dmpath}
         Returns the value / object at <dmpath>.

    PUT  /api/fluent_1/{dmpath}
         body: <json-value>
         Sets the value at <dmpath> (raw value, not wrapped).

    POST /api/fluent_1/{dmpath}
         body: { <command-args> }
         Executes a command at <dmpath>.

    DELETE /api/fluent_1/{path}
         Deletes the named object at <path>.

    GET  /api/fluent_1/{path}?attrs=attr1,attr2[&recursive=true]
         Returns attribute info for the setting at <path>.
         The server routes to ``getAttrs`` when the ``attrs`` query
         parameter is present.

Authentication
~~~~~~~~~~~~~~
Every request carries the header::

    Authorization: Bearer <sha256(auth_token)>

where *auth_token* is the password set when the Fluent session was started.

Error handling
~~~~~~~~~~~~~~
HTTP 4xx / 5xx responses raise :class:`FluentRestError`.
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
    """Raised when the Fluent REST server returns an error response.

    Parameters
    ----------
    status : int
        HTTP status code.
    message : str
        Error detail from the response body, or the raw reason phrase.
    """

    def __init__(self, status: int, message: str) -> None:
        self.status = status
        super().__init__(f"HTTP {status}: {message}")


class FluentRestClient:
    """Pure-Python HTTP client for the Fluent DataModel REST API.

    Standalone REST client for reading and writing Fluent solver settings
    via the embedded web server.  Each public method maps to exactly one
    HTTP endpoint as documented in ``SettingsServiceClientGuide.md``.

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
        """Percent-encode each segment of a slash-delimited path.

        Fluent object names may contain URL-sensitive characters such as
        spaces, ``#``, ``?``, or ``%``.  Each segment is individually
        quoted so the resulting URL is always valid.
        """
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
        """Extract a human-readable detail string from an HTTP error."""
        try:
            return json.loads(exc.read()).get("detail", exc.reason)
        except Exception:
            return exc.reason

    def _send_once(self, req: urllib.request.Request) -> Any:
        """Execute a single HTTP round-trip and return decoded JSON.

        Returns ``{}`` for empty 2xx bodies.

        Raises
        ------
        urllib.error.HTTPError
            On any non-2xx response.
        urllib.error.URLError
            On connection-level failures.
        """
        with urllib.request.urlopen(
            req, timeout=self._timeout, context=self._ssl_context
        ) as resp:  # nosec B310
            raw = resp.read()
            return json.loads(raw) if raw.strip() else {}

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        body: Any = None,
    ) -> Any:
        """Send an HTTP request with automatic retry and return the JSON body.

        Parameters
        ----------
        method : str
            HTTP verb (``"GET"``, ``"PUT"``, ``"POST"``, ``"DELETE"``).
        endpoint : str
            Path relative to *base_url*.
        body : any JSON-serialisable object, optional
            Request body.

        Returns
        -------
        Any
            Decoded JSON response, or ``{}`` for empty 2xx bodies.

        Raises
        ------
        FluentRestError
            For any HTTP 4xx / 5xx response after retries are exhausted.
        """
        url = self._url(endpoint)
        req = self._build_request(method, url, body)

        is_safe = method.upper() in _RETRYABLE_METHODS
        max_retries = self._max_retries if is_safe else 0

        last_exc: Exception | None = None
        for attempt in range(max_retries + 1):
            try:
                return self._send_once(req)
            except urllib.error.HTTPError as exc:
                detail = self._parse_error_detail(exc)
                if exc.code in _RETRYABLE_STATUS_CODES and attempt < max_retries:
                    wait = self._retry_delay * (2**attempt)
                    logger.warning(
                        "HTTP %d on %s %s — retry %d/%d in %.1fs",
                        exc.code,
                        method,
                        url,
                        attempt + 1,
                        max_retries,
                        wait,
                    )
                    time.sleep(wait)
                    last_exc = FluentRestError(exc.code, detail)
                    continue
                if not is_safe and exc.code in _RETRYABLE_STATUS_CODES:
                    logger.warning(
                        "HTTP %d on %s %s — non-idempotent, verify server state.",
                        exc.code,
                        method,
                        url,
                    )
                raise FluentRestError(exc.code, detail) from exc
            except urllib.error.URLError as exc:
                if attempt < max_retries:
                    wait = self._retry_delay * (2**attempt)
                    logger.warning(
                        "Connection error on %s %s: %s — retry %d/%d in %.1fs",
                        method,
                        url,
                        exc.reason,
                        attempt + 1,
                        max_retries,
                        wait,
                    )
                    time.sleep(wait)
                    last_exc = exc
                    continue
                if not is_safe:
                    logger.warning(
                        "Connection error on %s %s — non-idempotent, verify server state.",
                        method,
                        url,
                    )
                raise FluentRestError(0, str(exc.reason)) from exc

        raise last_exc  # type: ignore[misc]

    # ------------------------------------------------------------------
    # Settings API — read / write
    # ------------------------------------------------------------------

    def get_static_info(self) -> dict[str, Any]:
        """Return the full settings schema.

        Calls ``GET /api/{component}/static-info``.

        Returns
        -------
        dict[str, Any]
            A nested dict describing the settings tree structure, with keys
            such as ``"type"``, ``"children"``, ``"commands"``.
        """
        return self._request("GET", f"{self._api_base}/static-info")

    def get_var(self, path: str) -> Any:
        """Return the current value of the setting at *path*.

        Calls ``POST /api/{component}/get_var`` with body ``{"path": path}``.

        Parameters
        ----------
        path : str
            Slash-delimited settings path, e.g.
            ``"setup/models/energy/enabled"``.

        Returns
        -------
        Any
            The value at *path* — may be a bool, int, float, str, list, or
            dict (for group-level reads).

        Raises
        ------
        FluentRestError
            If the path does not exist (HTTP 404) or the server returns an
            error.
        """
        return self._request("POST", f"{self._api_base}/get_var", body={"path": path})

    def set_var(self, path: str, value: Any) -> None:
        """Set the value of the setting at *path*.

        Calls ``PUT /api/{component}/{path}`` with the value as the JSON body.
        The server expects the raw value directly, not wrapped in ``{"value": ...}``.

        Parameters
        ----------
        path : str
            Slash-delimited settings path.
        value : Any
            New value (bool, int, float, str, list, or dict).

        Raises
        ------
        FluentRestError
            If the server rejects the value (e.g. validation failure).
        """
        self._request("PUT", f"{self._api_base}/{self._encode_path(path)}", body=value)

    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return the requested attributes for the setting at *path*.

        Calls ``GET /api/{component}/{path}?attrs=attr1,attr2&recursive=true``.
        The server-side ``handleGet`` routes to ``getAttrs`` when the ``attrs``
        query parameter is present.

        Parameters
        ----------
        path : str
            Slash-delimited settings path.
        attrs : list[str]
            Attribute names to retrieve, e.g. ``["allowed-values"]``,
            ``["active?", "read-only?"]``.
        recursive : bool, optional
            If ``True``, include attributes of child nodes.  Defaults to
            ``False``.

        Returns
        -------
        dict
            A dict with an ``"attrs"`` key mapping to the requested
            attribute values, e.g.
            ``{"attrs": {"allowed-values": ["laminar", "k-epsilon", ...]}}``.

        Notes
        -----
        Attributes like ``active?`` and ``read-only?`` are solver-computed
        metadata and cannot be modified via :meth:`set_var`.
        """
        params = {"attrs": ",".join(attrs)}
        if recursive:
            params["recursive"] = "true"
        query = urllib.parse.urlencode(params)
        return self._request(
            "GET", f"{self._api_base}/{self._encode_path(path)}?{query}"
        )

    def get_object_names(self, path: str) -> list[str]:
        """Return the child named-object names at *path*.

        Calls ``GET /api/{component}/{path}`` and extracts the object names
        from the response dict keys.

        Parameters
        ----------
        path : str
            Path to a named-object container, e.g.
            ``"setup/boundary-conditions/velocity-inlet"``.

        Returns
        -------
        list[str]
            Sorted or insertion-order list of child names.  Returns ``[]``
            if the path does not exist (HTTP 404).

        Raises
        ------
        FluentRestError
            If the server returns an unexpected error.
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

    def create(self, path: str, name: str) -> None:
        """Create a named child object *name* at *path*.

        Calls ``POST /api/{component}/{path}`` with body ``{"name": name}``.

        Parameters
        ----------
        path : str
            Path to the named-object container.
        name : str
            Name of the new child object.

        Raises
        ------
        FluentRestError
            If the server rejects the creation.
        """
        self._request(
            "POST", f"{self._api_base}/{self._encode_path(path)}", body={"name": name}
        )

    def delete(self, path: str, name: str, *, ignore_not_found: bool = False) -> None:
        """Delete the named child object *name* at *path*.

        Calls ``DELETE /api/{component}/{path}/{name}``.

        Parameters
        ----------
        path : str
            Path to the named-object container.
        name : str
            Name of the child object to delete.
        ignore_not_found : bool, optional
            If ``True``, silently ignore HTTP 404 (object already absent).
            Defaults to ``False``, but
            callers performing idempotent cleanup should pass ``True``.

        Raises
        ------
        FluentRestError
            If *ignore_not_found* is ``False`` and the object does not exist
            (HTTP 404), or on any other server error.
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
        """Rename a child object at *path* from *old* to *new*.

        Calls ``PUT /api/{component}/{path}/{old}`` with body
        ``{"name": new}``.

        Parameters
        ----------
        path : str
            Path to the named-object container.
        new : str
            New name for the child object.
        old : str
            Current name of the child object.

        Raises
        ------
        FluentRestError
            If the object *old* does not exist.
        """
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
        """Delete specific named children of *obj_type* under *path*.

        Calls ``DELETE /api/{component}/{path}/{obj_type}/{name}`` once for
        each entry in *child_names*.  Equivalent to deleting a specific
        list of named child objects.

        Parameters
        ----------
        path : str
            Path to the parent container, e.g. ``"setup/boundary-conditions"``.
        obj_type : str
            Child object type (sub-container name), e.g. ``"velocity-inlet"``.
        child_names : list[str]
            Names of the child objects to delete.

        Raises
        ------
        FluentRestError
            If any individual delete fails (e.g. HTTP 404 — object not found).
        """
        for name in child_names:
            self.delete(f"{path}/{obj_type}", name)

    def delete_all_child_objects(self, path: str, obj_type: str) -> None:
        """Delete all named children of *obj_type* under *path*.

        Discovers children via :meth:`get_object_names` and then calls
        :meth:`delete_child_objects` for all of them.  Equivalent to
        deleting every child at once.

        Parameters
        ----------
        path : str
            Path to the parent container, e.g. ``"setup/boundary-conditions"``.
        obj_type : str
            Child object type (sub-container name), e.g. ``"velocity-inlet"``.

        Raises
        ------
        FluentRestError
            If any individual delete fails.
        """
        names = self.get_object_names(f"{path}/{obj_type}")
        self.delete_child_objects(path, obj_type, names)

    def get_list_size(self, path: str) -> int:
        """Return the number of elements in the list-object at *path*.

        Calls ``GET /api/{component}/{path}`` and counts the entries.

        .. note::

            This method makes an independent ``GET`` request rather than
            delegating to :meth:`get_object_names` because it also handles
            list-objects that carry a ``"size"`` key and raw arrays, which
            ``get_object_names`` does not support.

        Parameters
        ----------
        path : str
            Path to a named-object container or list-object.

        Returns
        -------
        int
            Number of child objects.  Returns ``0`` if the path does not
            exist (HTTP 404).

        Raises
        ------
        FluentRestError
            If the server returns an unexpected error.
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
        """Resize the list-object at *path* to *size* elements.

        Calls ``POST /api/{component}/{path}`` with body
        ``{"new-size": size}``.

        Parameters
        ----------
        path : str
            Path to the list-object.
        size : int
            Desired number of elements.

        Raises
        ------
        FluentRestError
            If the server rejects the resize.
        """
        self._request(
            "POST",
            f"{self._api_base}/{self._encode_path(path)}",
            body={"new-size": size},
        )

    def _execute(self, path: str, name: str, **kwds) -> Any:
        """Post a command or query and return the ``"reply"`` payload.

        Retries automatically when the server returns
        ``400 Fluent not running`` — the solver may still be initialising
        after the web server port opened.  Gives up after *_SOLVER_READY_TIMEOUT*
        seconds and re-raises the original error.
        """
        _SOLVER_READY_TIMEOUT = 120  # seconds
        _SOLVER_RETRY_DELAY = 5  # seconds between retries
        start = time.monotonic()
        while True:
            try:
                encoded_name = urllib.parse.quote(name, safe="")
                result = self._request(
                    "POST",
                    f"{self._api_base}/{self._encode_path(path)}/{encoded_name}",
                    body=kwds,
                )
                return result.get("reply") if isinstance(result, dict) else result
            except FluentRestError as exc:
                elapsed = time.monotonic() - start
                if (
                    exc.status == 400
                    and "Fluent not running" in str(exc)
                    and elapsed < _SOLVER_READY_TIMEOUT
                ):
                    logger.debug(
                        "Solver not ready yet (400 Fluent not running) — "
                        "retrying in %ds (elapsed=%.0fs / %ds)...",
                        _SOLVER_RETRY_DELAY,
                        elapsed,
                        _SOLVER_READY_TIMEOUT,
                    )
                    time.sleep(_SOLVER_RETRY_DELAY)
                    continue
                raise

    def execute_cmd(self, path: str, command: str, **kwds) -> Any:
        """Execute *command* at *path* with keyword arguments.

        Calls ``POST /api/{component}/{path}/{command}`` with body ``kwds``.

        Parameters
        ----------
        path : str
            Path to the parent object containing the command.
        command : str
            Command name, e.g. ``"initialize"``.
        **kwds
            Arbitrary keyword arguments forwarded as the JSON request body.

        Returns
        -------
        Any
            The ``"reply"`` field from the response, or the raw response
            if no ``"reply"`` key is present.

        Raises
        ------
        FluentRestError
            If the server rejects the command (e.g. HTTP 409 conflict).
        """
        return self._execute(path, command, **kwds)

    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute *query* at *path* with keyword arguments.

        Calls ``POST /api/{component}/{path}/{query}`` with body ``kwds``.

        Parameters
        ----------
        path : str
            Path to the parent object containing the query.
        query : str
            Query name, e.g. ``"get-zone-names"``.
        **kwds
            Arbitrary keyword arguments forwarded as the JSON request body.

        Returns
        -------
        Any
            The ``"reply"`` field from the response, or the raw response
            if no ``"reply"`` key is present.

        Raises
        ------
        FluentRestError
            If the server rejects the query.
        """
        return self._execute(path, query, **kwds)

    # ------------------------------------------------------------------
    # Local helpers (no server round-trip)
    # ------------------------------------------------------------------

    def has_wildcard(self, name: str) -> bool:
        """Return ``True`` if *name* contains an ``fnmatch``-style wildcard.

        Recognised wildcard characters: ``*``, ``?``, ``[``.
        Performs the check locally — no server round-trip required.

        Parameters
        ----------
        name : str
            The name to check.

        Returns
        -------
        bool
            ``True`` if *name* contains a wildcard character.
        """
        return any(c in name for c in ("*", "?", "["))

    def is_interactive_mode(self) -> bool:
        """Query the server's run mode to determine interactivity.

        Calls ``GET /api/connection/run_mode`` and returns ``True`` if
        the server reports an interactive mode.  Falls back to ``False``
        on any connection or parse error.

        Returns
        -------
        bool
            ``True`` if the server is in interactive mode.
        """
        try:
            result = self._request("GET", "api/connection/run_mode")
            if isinstance(result, dict):
                return bool(result.get("interactive", False))
            return False
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------

    def exit(self, force: bool = True) -> None:
        """Gracefully shut down the Fluent session.

        Sends ``POST /api/connection/exit`` to ask the server to
        terminate.  The server handles its own process cleanup.

        Parameters
        ----------
        force : bool, optional
            If ``True`` (default), appends ``?force=true`` to skip any
            confirmation prompt the server might require.

        Raises
        ------
        FluentRestError
            HTTP 403 if exit is blocked (e.g. calculation running),
            or HTTP 409 if a confirmation prompt is needed and
            *force* is ``False``.
        """
        endpoint = "api/connection/exit"
        if force:
            endpoint += "?force=true"
        try:
            self._request("POST", endpoint)
            logger.info("Sent /exit to Fluent server.")
        except FluentRestError as exc:
            if exc.status in (403, 409):
                raise
            logger.debug("Server /exit request failed (HTTP %d).", exc.status)
        except Exception:
            logger.debug("Server /exit request failed (may already be down).")

    def __enter__(self) -> "FluentRestClient":
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager — calls :meth:`exit`."""
        self.exit()
