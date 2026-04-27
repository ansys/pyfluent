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

Fluent embeds an HTTP server (SimBA - Simulation Bridge Application) that
serves the solver settings via a DataModel REST API.  The base path for all
settings endpoints is ``/api/{component}/`` where *component* is ``"fluent_1"``
for a solver session (``"fluent_meshing_1"`` for a meshing session).

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
         body: { "value": <json-value> }
         Sets the value at <dmpath>.

    POST /api/fluent_1/{dmpath}
         body: { <command-args> }
         Executes a command at <dmpath>.

    DELETE /api/fluent_1/{path}
         Deletes the named object at <path>.

    POST /api/fluent_1/get_attrs
         body: { "path": "<path>", "attrs": [<str>, ...] }
         Returns attribute info for the setting at <path>.

Authentication
~~~~~~~~~~~~~~
Every request carries the header::

    Authorization: Bearer <auth_token>

where *auth_token* is the password set when the Fluent session was started.

Error handling
~~~~~~~~~~~~~~
HTTP 4xx / 5xx responses raise :class:`FluentRestError`.
"""

import json
from typing import Any
import urllib.error
import urllib.parse
import urllib.request


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

    The public method signatures are intentionally identical to the duck-typed
    *flproxy* interface consumed by
    :func:`~ansys.fluent.core.solver.flobject.get_root`, so this client can be
    passed directly as *flproxy* to build the full settings tree over HTTP
    instead of gRPC.

    Parameters
    ----------
    base_url : str
        Root URL of the Fluent REST server, e.g. ``"http://10.18.44.175:5000"``.
        A trailing slash is stripped automatically.
    auth_token : str, optional
        Bearer token (the password set when Fluent was started).  Added to
        every request as ``Authorization: Bearer ...``.
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"`` (solver).
        Use ``"fluent_meshing_1"`` for a meshing session.
    timeout : float, optional
        Socket timeout in seconds for every request.  Defaults to ``30.0``.

    Examples
    --------
    >>> from ansys.fluent.core.rest import FluentRestClient, FluentRestMockServer
    >>> server = FluentRestMockServer().start()
    >>> client = FluentRestClient(server.base_url)
    >>> client.get_var("setup/models/energy/enabled")
    True
    >>> client.set_var("setup/models/energy/enabled", False)
    >>> server.stop()
    """

    def __init__(
        self,
        base_url: str,
        *,
        auth_token: str | None = None,
        component: str = "fluent_1",
        timeout: float = 30.0,
    ) -> None:
        parsed = urllib.parse.urlparse(base_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("base_url scheme must be http or https")
        if not parsed.netloc:
            raise ValueError("base_url must include host")
        self._base_url = base_url.rstrip("/")
        self._auth_token = auth_token
        self._component = component
        self._timeout = timeout
        # All DataModel endpoints live under this prefix, e.g. "api/fluent_1"
        self._api_base = f"api/{component}"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _url(self, endpoint: str) -> str:
        """Build a full URL from *endpoint*."""
        return f"{self._base_url}/{endpoint}"

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        body: Any = None,
    ) -> Any:
        """Send an HTTP request and return the decoded JSON response body.

        Parameters
        ----------
        method : str
            HTTP verb (``"GET"``, ``"PUT"``, ``"POST"``, ``"DELETE"``).
        endpoint : str
            Path relative to *base_url*, e.g. ``"api/fluent_1/static-info"``.
        body : any JSON-serialisable object, optional
            Request body; encoded as UTF-8 JSON.

        Returns
        -------
        dict
            Decoded JSON response, or ``{}`` for empty 2xx bodies.

        Raises
        ------
        FluentRestError
            For any HTTP 4xx or 5xx response.
        """
        url = self._url(endpoint)
        data: bytes | None = None
        headers: dict[str, str] = {}

        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        if self._auth_token:
            headers["Authorization"] = f"Bearer {self._auth_token}"

        req = urllib.request.Request(
            url, data=data, headers=headers, method=method.upper()
        )
        try:
            with urllib.request.urlopen(
                req, timeout=self._timeout
            ) as resp:  # nosec B310
                raw = resp.read()
                return json.loads(raw) if raw.strip() else {}
        except urllib.error.HTTPError as exc:
            try:
                detail = json.loads(exc.read()).get("detail", exc.reason)
            except Exception:
                detail = exc.reason
            raise FluentRestError(exc.code, detail) from exc

    # ------------------------------------------------------------------
    # flobject proxy interface
    # ------------------------------------------------------------------

    def get_static_info(self) -> dict[str, Any]:
        """Return the full settings schema.

        Calls ``GET /api/{component}/static-info``.
        """
        return self._request("GET", f"{self._api_base}/static-info")

    def get_var(self, path: str) -> Any:
        """Return the current value of the setting at *path*.

        Calls ``POST /api/{component}/get_var`` with body ``{"path": path}``.
        """
        return self._request("POST", f"{self._api_base}/get_var", body={"path": path})

    def set_var(self, path: str, value: Any) -> None:
        """Set the value of the setting at *path*.

        Calls ``PUT /api/{component}/{path}`` with body ``{"value": value}``.
        """
        self._request("PUT", f"{self._api_base}/{path}", body={"value": value})

    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return the requested attributes for the setting at *path*.

        Calls ``POST /api/{component}/get_attrs`` with body
        ``{"path": path, "attrs": attrs}``.
        """
        return self._request(
            "POST",
            f"{self._api_base}/get_attrs",
            body={"path": path, "attrs": attrs, "recursive": recursive},
        )

    def get_object_names(self, path: str) -> list[str]:
        """Return the child named-object names at *path*.

        Calls ``GET /api/{component}/{path}`` and returns the list of names.
        Returns an empty list if the path does not exist.
        """
        try:
            result = self._request("GET", f"{self._api_base}/{path}")
        except FluentRestError as exc:
            if exc.status == 404:
                return []
            raise
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            # Named objects are returned as dict with object names as keys
            return list(result.keys())
        return []

    def create(self, path: str, name: str) -> None:
        """Create a named child object *name* at *path*.

        Calls ``POST /api/{component}/{path}`` with body ``{"name": name}``.
        """
        self._request("POST", f"{self._api_base}/{path}", body={"name": name})

    def delete(self, path: str, name: str) -> None:
        """Delete the named child object *name* at *path*.

        Calls ``DELETE /api/{component}/{path}/{name}``.
        """
        self._request("DELETE", f"{self._api_base}/{path}/{name}")

    def rename(self, path: str, new: str, old: str) -> None:
        """Rename a child object at *path* from *old* to *new*.

        Calls ``PUT /api/{component}/{path}`` with body
        ``{"rename": {"new": new, "old": old}}``.
        """
        self._request(
            "PUT",
            f"{self._api_base}/{path}",
            body={"rename": {"new": new, "old": old}},
        )

    def get_list_size(self, path: str) -> int:
        """Return the number of elements in the list-object at *path*.

        Calls ``GET /api/{component}/{path}`` and reads the list length.
        Returns ``0`` if the path does not exist.
        """
        try:
            result = self._request("GET", f"{self._api_base}/{path}")
        except FluentRestError as exc:
            if exc.status == 404:
                return 0
            raise
        if isinstance(result, list):
            return len(result)
        if isinstance(result, dict):
            # Named-object containers return dict with names as keys
            # List-objects with explicit size return {"size": n}
            if "size" in result:
                return result["size"]
            # Named objects: count the keys (object names)
            return len(result)
        return 0

    def resize_list_object(self, path: str, size: int) -> None:
        """Resize the list-object at *path* to *size* elements.

        Calls ``PUT /api/{component}/{path}`` with body ``{"size": size}``.
        """
        self._request("PUT", f"{self._api_base}/{path}", body={"size": size})

    def execute_cmd(self, path: str, command: str, **kwds) -> Any:
        """Execute *command* at *path* with keyword arguments *kwds*.

        Calls ``POST /api/{component}/{path}/{command}`` with body ``kwds``.
        """
        result = self._request(
            "POST", f"{self._api_base}/{path}/{command}", body=kwds
        )
        return result.get("reply") if isinstance(result, dict) else result

    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute *query* at *path* with keyword arguments *kwds*.

        Calls ``POST /api/{component}/{path}/{query}`` with body ``kwds``.
        """
        result = self._request("POST", f"{self._api_base}/{path}/{query}", body=kwds)
        return result.get("reply") if isinstance(result, dict) else result

    # ------------------------------------------------------------------
    # Additional proxy interface helpers (no server round-trip required)
    # ------------------------------------------------------------------

    def has_wildcard(self, name: str) -> bool:
        """Return ``True`` if *name* contains an ``fnmatch``-style wildcard.

        Recognised wildcard characters: ``*``, ``?``, ``[``.
        Performs the check locally – no server round-trip required.
        """
        return any(c in name for c in ("*", "?", "["))

    def is_interactive_mode(self) -> bool:
        """Check if server is running in interactive mode.
        
        Queries ``/api/connection/run_mode`` and returns True if the mode
        is not 'batch'. Returns False on error or if mode is 'batch'.
        """
        try:
            # Use the connection endpoint (not under component prefix)
            url = f"{self._base_url}/api/connection/run_mode"
            headers = {}
            if self._auth_token:
                headers["Authorization"] = f"Bearer {self._auth_token}"
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = resp.read()
                mode = json.loads(data) if data.strip() else ""
            
            # Fluent returns "fluent_proxy", "interactive", etc. for interactive mode
            # and "batch" for batch mode
            return mode != "batch"
        except Exception:
            # If we can't determine mode, assume non-interactive (safe default)
            return False
