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

"""Fluent settings REST API client.

This module is intentionally free of HTTP mechanics.  All transport
concerns (auth, retry, SSL) live in
:mod:`~ansys.fluent.core.rest.transport`.  Inject any
:class:`~ansys.fluent.core.rest.transport.RequestStrategy` — including a
lightweight test double — to exercise the API layer in isolation.

Typical use::

    >>> client = FluentRestClient.connect("http://127.0.0.1:5000", auth_token="secret")
    >>> client.get_var("setup/models/energy/enabled")
"""

import logging
import ssl
from typing import Any
import urllib.parse

from ansys.fluent.core.rest.errors import FluentRestError
from ansys.fluent.core.rest.transport import HttpRequestStrategy, RequestStrategy

logger = logging.getLogger(__name__)


class FluentRestClient:
    """Fluent DataModel settings API client.

    The client is decoupled from HTTP mechanics via an injected
    :class:`~ansys.fluent.core.rest.transport.RequestStrategy`.  In
    production, use :meth:`connect` to assemble the real stack.  In
    tests, pass any object whose ``request`` method matches the protocol.

    Parameters
    ----------
    strategy : RequestStrategy
        Responsible for executing HTTP requests (real or fake).
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"`` (solver).
        Use ``"fluent_meshing_1"`` for a meshing session.
    """

    def __init__(
        self,
        strategy: RequestStrategy,
        *,
        component: str = "fluent_1",
    ) -> None:
        self._strategy = strategy
        self._api_base = f"api/{component}"

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def connect(
        cls,
        url: str,
        auth_token: str,
        *,
        component: str = "fluent_1",
        timeout: float = 30.0,
        max_retries: int = 2,
        retry_delay: float = 1.0,
        ssl_context: ssl.SSLContext | None = None,
    ) -> "FluentRestClient":
        """Create a client connected to an already-running Fluent REST server.

        This is a convenience factory that assembles an
        :class:`~ansys.fluent.core.rest.transport.HttpRequestStrategy` and
        wires it into a new :class:`FluentRestClient`.  For testing,
        construct directly with a fake strategy instead.

        Parameters
        ----------
        url : str
            Full URL of the Fluent REST server, e.g.
            ``"http://127.0.0.1:5000"``.
        auth_token : str
            Bearer token (password) set when Fluent was started.
        component : str, optional
            DataModel component name. Defaults to ``"fluent_1"``.
        timeout : float, optional
            Socket timeout in seconds. Defaults to ``30.0``.
        max_retries : int, optional
            Maximum automatic retries on transient failures. Defaults to
            ``2``.
        retry_delay : float, optional
            Base delay between retries (exponential back-off). Defaults to
            ``1.0``.
        ssl_context : ssl.SSLContext, optional
            Custom SSL context for HTTPS connections.
        """
        logger.info("Connecting to Fluent REST server at %s", url)
        strategy = HttpRequestStrategy(
            url,
            auth_token=auth_token,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            ssl_context=ssl_context,
        )
        return cls(strategy, component=component)

    # ------------------------------------------------------------------
    # Settings API — read / write
    # ------------------------------------------------------------------

    def get_static_info(self, full: bool = False) -> dict[str, Any]:
        """Return the full settings schema (GET static-info)."""
        endpoint = f"{self._api_base}/static-info"
        if full:
            endpoint += "?full=true"
        return self._strategy.request("GET", endpoint)

    def get_var(self, path: str) -> Any:
        """Return the value at *path* (POST ``get_var``)."""
        return self._strategy.request(
            "POST", f"{self._api_base}/get_var", body={"path": path.lstrip("/")}
        )

    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> Any:
        """Return selected attributes for *path* (GET with ``attrs=...``)."""
        params = {"attrs": ",".join(attrs)}
        if recursive:
            params["recursive"] = "true"
        query = urllib.parse.urlencode(params)
        return self._strategy.request("GET", f"{self._api_base}/{path}?{query}")

    def get_object_names(self, path: str) -> list[str]:
        """Return child object names at *path*; ``[]`` on 404.

        Raises
        ------
        FluentRestError
            If the request fails with a non-404 HTTP error.
        """
        result = self._strategy.request("GET", f"{self._api_base}/{path}")
        return _names_from(result)

    def get_list_size(self, path: str) -> int:
        """Return element count at *path*; ``0`` on 404.

        Raises
        ------
        FluentRestError
            If the request fails with a non-404 HTTP error.
        """
        result = self._strategy.request("GET", f"{self._api_base}/{path}")
        return _size_from(result)

    def set_var(self, path: str, value: Any) -> None:
        """Write value at DataModel path.

        Parameters
        ----------
        path : str
            DataModel path where the value will be written (e.g.,
            ``"setup/models/viscous/model"``).
        value : Any
            Value to write. This will be JSON-encoded in the request body.

        Raises
        ------
        FluentRestError
            If the request fails. Returns HTTP 404 if the DataModel path
            does not exist.
        """
        self._strategy.request("PUT", f"{self._api_base}/{path}", body=value)

    def resize_list_object(self, path: str, size: int) -> None:
        """Resize the list-object at *path* to *size* elements (POST ``{path}``)."""
        self._strategy.request(
            "POST", f"{self._api_base}/{path}", body={"new-size": size}
        )

    # ------------------------------------------------------------------
    # Settings API — named objects CRUD
    # ------------------------------------------------------------------

    def create(
        self, path: str, name: str = "", properties: dict[str, Any] | None = None
    ) -> Any:
        """Create a child object at DataModel path.

        Parameters
        ----------
        path : str
            DataModel path where the object will be created (e.g.,
            ``"setup/boundary_conditions/velocity_inlet"``).
        name : str, optional
            Name for the created object. If provided, it is merged into the
            request body. Defaults to ``""``.
        properties : dict[str, Any] | None, optional
            Properties to set on creation. These are merged with the ``name``
            parameter in the request body. Defaults to ``None``.

        Returns
        -------
        Any
            Server response containing details of the created object.

        Raises
        ------
        FluentRestError
            If the request fails.
        """
        body = dict(properties) if properties else {}
        if name:
            body["name"] = name
        return self._strategy.request("POST", f"{self._api_base}/{path}", body=body)

    def delete(self, path: str, name: str, *, ignore_not_found: bool = False) -> None:
        """Delete named object from DataModel path.

        Parameters
        ----------
        path : str
            DataModel path containing the object (e.g.,
            ``"setup/boundary_conditions/velocity_inlet"``).
        name : str
            Name of the object to delete (e.g., ``"inlet_1"``).
        ignore_not_found : bool, optional
            If ``True``, suppress ``FluentRestError`` when object not found (404).
            Defaults to ``False``.

        Raises
        ------
        FluentRestError
            If deletion fails, except when ``ignore_not_found=True`` and the
            server returns HTTP 404.
        """
        try:
            endpoint = f"{self._api_base}/{path}/{urllib.parse.quote(name, safe='')}"
            self._strategy.request("DELETE", endpoint)
        except FluentRestError as exc:
            if not (ignore_not_found and exc.status == 404):
                raise

    def rename(self, path: str, new: str, old: str) -> None:
        """Rename object from *old* to *new* at DataModel path.

        Parameters
        ----------
        path : str
            DataModel path containing the object (e.g.,
            ``"setup/boundary_conditions/velocity_inlet"``).
        new : str
            New name for the object.
        old : str
            Current name of the object to rename.

        Raises
        ------
        FluentRestError
            If the rename operation fails.
        """
        self._strategy.request(
            "PUT",
            f"{self._api_base}/{path}/{urllib.parse.quote(old, safe='')}",
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
        self.delete_child_objects(
            path, obj_type, self.get_object_names(f"{path}/{obj_type}")
        )

    # ------------------------------------------------------------------
    # Commands / queries
    # ------------------------------------------------------------------

    def _execute(self, path: str, name: str, **kwds) -> Any:
        """POST a command/query endpoint and return the raw response payload."""
        endpoint = f"{self._api_base}/{path}/{urllib.parse.quote(name, safe='')}"
        return self._strategy.request("POST", endpoint, body=kwds)

    def execute_cmd(self, path: str, command: str, force: bool = True, **kwds) -> Any:
        """Execute *command* at *path*; appends ``?force=true`` when requested."""
        endpoint = f"{self._api_base}/{path}/{urllib.parse.quote(command, safe='')}"
        if force:
            endpoint += "?force=true"
        return self._strategy.request("POST", endpoint, body=kwds)

    def execute_query(self, path: str, query: str, **kwds) -> Any:
        """Execute *query* at *path* (POST {path}/{query})."""
        return self._execute(path, query, **kwds)


# ------------------------------------------------------------------
# Response helpers — module-level pure functions, independently testable
# ------------------------------------------------------------------


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
