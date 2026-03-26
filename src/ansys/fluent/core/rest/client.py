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

"""Pure-Python REST client for Fluent solver settings.

Provisional REST API Contract
------------------------------
All endpoints share the base URL ``<base_url>/settings``.  JSON is used for
both request bodies and response payloads.  When a real Fluent REST API is
published, only the constants in :data:`_Endpoints` and the helper
:meth:`FluentRestClient._request` need updating.

Endpoint summary
~~~~~~~~~~~~~~~~

.. code-block:: text

    GET  /settings/static-info
         → { "info": <static-info-dict> }

    GET  /settings/var?path=<path>
         → { "value": <json-value> }

    PUT  /settings/var?path=<path>
         body: { "value": <json-value> }
         → {}

    GET  /settings/attrs?path=<path>&attrs=<a1>&attrs=<a2>[&recursive=true]
         → { "attrs": <json-value>, "group_children": {...} }   (group_children
            only present when recursive=true)

    GET  /settings/object-names?path=<path>
         → { "names": [<str>, ...] }

    POST /settings/create?path=<path>&name=<name>
         → {}

    DELETE /settings/object?path=<path>&name=<name>
         → {}

    PATCH /settings/rename?path=<path>
          body: { "new": <str>, "old": <str> }
          → {}

    GET  /settings/list-size?path=<path>
         → { "size": <int> }

    POST /settings/commands/<cmd>?path=<path>
         body: { <kwarg-key>: <value>, ... }
         → { "reply": <json-value> }

    POST /settings/queries/<query>?path=<path>
         body: { <kwarg-key>: <value>, ... }
         → { "reply": <json-value> }

Authentication
~~~~~~~~~~~~~~
When *auth_token* is supplied, every request carries the header::

    Authorization: Bearer <auth_token>

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


class _Endpoints:
    """Centralised endpoint paths – update here when the real spec ships."""

    BASE = "settings"
    STATIC_INFO = "settings/static-info"
    VAR = "settings/var"
    ATTRS = "settings/attrs"
    OBJECT_NAMES = "settings/object-names"
    CREATE = "settings/create"
    DELETE = "settings/object"
    RENAME = "settings/rename"
    LIST_SIZE = "settings/list-size"
    COMMANDS = "settings/commands"
    QUERIES = "settings/queries"


class FluentRestClient:
    """Pure-Python HTTP client for Fluent solver settings.

    The public method signatures are intentionally identical to the duck-typed
    *flproxy* interface consumed by
    :func:`~ansys.fluent.core.solver.flobject.get_root`, so this client can be
    passed directly as *flproxy* in Step 2 of the componentisation work.

    Parameters
    ----------
    base_url : str
        Root URL of the Fluent REST server, e.g. ``"http://localhost:8000"``.
        A trailing slash is stripped automatically.
    auth_token : str, optional
        Bearer token added to every request as ``Authorization: Bearer …``.
    timeout : float, optional
        Socket timeout in seconds for every request.  Defaults to ``30.0``.

    Examples
    --------
    >>> from ansys.fluent.core.rest import FluentRestClient, FluentRestMockServer
    >>> server = FluentRestMockServer()
    >>> server.start()
    >>> client = FluentRestClient(f"http://localhost:{server.port}")
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
        timeout: float = 30.0,
    ) -> None:
        parsed = urllib.parse.urlparse(base_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("base_url scheme must be http or https")
        if not parsed.netloc:
            raise ValueError("base_url must include host")
        self._base_url = base_url.rstrip("/")
        self._auth_token = auth_token
        self._timeout = timeout

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _url(self, endpoint: str, **query_params) -> str:
        """Build a full URL from *endpoint* and optional query params."""
        url = f"{self._base_url}/{endpoint}"
        # urllib.parse.urlencode does not support multi-value keys natively
        # when passed a dict, but doseq=True handles list values.
        if query_params:
            # Convert single values to strings; keep lists as-is for doseq.
            encoded = urllib.parse.urlencode(
                {k: v for k, v in query_params.items() if v is not None},
                doseq=True,
            )
            url = f"{url}?{encoded}"
        return url

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        query_params: dict | None = None,
        body: Any = None,
    ) -> Any:
        """Send an HTTP request and return the decoded JSON response body.

        Parameters
        ----------
        method : str
            HTTP verb (``"GET"``, ``"PUT"``, ``"POST"``, ``"PATCH"``,
            ``"DELETE"``).
        endpoint : str
            Path relative to *base_url*, e.g. ``"settings/var"``.
        query_params : dict, optional
            Mapping of URL query parameters.  List values produce repeated
            keys (``?attrs=a&attrs=b``).
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
        url = self._url(endpoint, **(query_params or {}))
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
                detail = json.loads(exc.read()).get("error", exc.reason)
            except Exception:
                detail = exc.reason
            raise FluentRestError(exc.code, detail) from exc

    # ------------------------------------------------------------------
    # flobject proxy interface
    # ------------------------------------------------------------------

    def get_static_info(self) -> dict[str, Any]:
        """Return the full static-info tree for all solver settings.

        Corresponds to ``GET /settings/static-info``.
        """
        return self._request("GET", _Endpoints.STATIC_INFO)["info"]

    def get_var(self, path: str) -> Any:
        """Return the current value of the setting at *path*.

        Corresponds to ``GET /settings/var?path=<path>``.
        """
        return self._request("GET", _Endpoints.VAR, query_params={"path": path})[
            "value"
        ]

    def set_var(self, path: str, value: Any) -> None:
        """Set the value of the setting at *path*.

        Corresponds to ``PUT /settings/var?path=<path>`` with body
        ``{"value": <value>}``.
        """
        self._request(
            "PUT",
            _Endpoints.VAR,
            query_params={"path": path},
            body={"value": value},
        )

    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return the requested attributes for the setting at *path*.

        Corresponds to
        ``GET /settings/attrs?path=<path>&attrs=<a1>&attrs=<a2>[&recursive=true]``.
        """
        return self._request(
            "GET",
            _Endpoints.ATTRS,
            query_params={
                "path": path,
                "attrs": attrs,
                "recursive": str(recursive).lower(),
            },
        )

    def get_object_names(self, path: str) -> list[str]:
        """Return the child named-object names at *path*.

        Corresponds to ``GET /settings/object-names?path=<path>``.
        """
        return self._request(
            "GET", _Endpoints.OBJECT_NAMES, query_params={"path": path}
        )["names"]

    def create(self, path: str, name: str) -> None:
        """Create a named child object at *path*.

        Corresponds to ``POST /settings/create?path=<path>&name=<name>``.
        """
        self._request(
            "POST", _Endpoints.CREATE, query_params={"path": path, "name": name}
        )

    def delete(self, path: str, name: str) -> None:
        """Delete the named child object at *path*.

        Corresponds to ``DELETE /settings/object?path=<path>&name=<name>``.
        """
        self._request(
            "DELETE", _Endpoints.DELETE, query_params={"path": path, "name": name}
        )

    def rename(self, path: str, new: str, old: str) -> None:
        """Rename a child object at *path* from *old* to *new*.

        Corresponds to ``PATCH /settings/rename?path=<path>`` with body
        ``{"new": <new>, "old": <old>}``.
        """
        self._request(
            "PATCH",
            _Endpoints.RENAME,
            query_params={"path": path},
            body={"new": new, "old": old},
        )

    def get_list_size(self, path: str) -> int:
        """Return the number of elements in the list-object at *path*.

        Corresponds to ``GET /settings/list-size?path=<path>``.
        """
        return self._request("GET", _Endpoints.LIST_SIZE, query_params={"path": path})[
            "size"
        ]

    def execute_cmd(self, path: str, command: str, **kwds) -> Any:
        """Execute *command* at *path* with keyword arguments *kwds*.

        Corresponds to
        ``POST /settings/commands/<command>?path=<path>`` with body
        ``{<kwarg>: <value>, ...}``.
        """
        return self._request(
            "POST",
            f"{_Endpoints.COMMANDS}/{command}",
            query_params={"path": path},
            body=kwds,
        ).get("reply")

    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute *query* at *path* with keyword arguments *kwds*.

        Corresponds to
        ``POST /settings/queries/<query>?path=<path>`` with body
        ``{<kwarg>: <value>, ...}``.
        """
        return self._request(
            "POST",
            f"{_Endpoints.QUERIES}/{query}",
            query_params={"path": path},
            body=kwds,
        ).get("reply")

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
        """Always returns ``False`` for a REST client."""
        return False
