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

"""Lightweight solver session backed by a REST transport.

:class:`RestSolverSession` is a self-contained session object that wires
:class:`~ansys.fluent.core.rest.client.FluentRestClient` into
:func:`~ansys.fluent.core.solver.flobject.get_root` so the full settings tree
works over HTTP instead of gRPC.

It intentionally does **not** inherit from
:class:`~ansys.fluent.core.session_solver.Solver` or
:class:`~ansys.fluent.core.fluent_connection.FluentConnection` — those classes
carry ~15 gRPC-coupled constructor arguments.  ``RestSolverSession`` needs only
a *base_url* (and optionally *auth_token* and *version*).

Usage
-----
::

    from ansys.fluent.core.rest.rest_session import RestSolverSession

    session = RestSolverSession("http://127.0.0.1:54321", version="261")
    print(session.settings.setup.models.energy.enabled())
"""

from __future__ import annotations

import logging
import subprocess
import time
from typing import TYPE_CHECKING

from ansys.fluent.core.rest.client import FluentRestClient
from ansys.fluent.core.solver.flobject import get_root

if TYPE_CHECKING:
    from ansys.fluent.core.solver.flobject import Group

logger = logging.getLogger(__name__)

__all__ = ["RestSolverSession"]


class RestSolverSession:
    """Solver session that communicates over REST.

    Builds a :class:`FluentRestClient`, passes it as *flproxy* to
    :func:`~ansys.fluent.core.solver.flobject.get_root`, and exposes the
    resulting settings tree via :attr:`settings`.

    Parameters
    ----------
    base_url : str
        Root URL of the Fluent REST server, e.g. ``"http://127.0.0.1:54321"``.
    auth_token : str, optional
        Bearer token for authentication.
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"``.
    version : str, optional
        Fluent version string (e.g. ``"261"``).  Passed through to
        ``get_root`` so the correct code-generated settings module is loaded
        when available.
    timeout : float, optional
        HTTP socket timeout in seconds.  Defaults to ``30.0``.
    max_retries : int, optional
        Maximum automatic retries on transient errors.  Defaults to ``0``.
    retry_delay : float, optional
        Base delay in seconds between retries.  Defaults to ``1.0``.

    Attributes
    ----------
    settings : Group
        Root of the solver settings tree.
    client : FluentRestClient
        The underlying REST transport proxy.
    ip : str
        IP address of the connected server.  Set by :func:`launch_webserver`
        or :func:`connect_to_webserver`; otherwise ``None``.
    port : int | None
        Port of the connected server.  Set by :func:`launch_webserver`
        or :func:`connect_to_webserver`; otherwise ``None``.
    auth_token : str | None
        Auth token used for the connection.  Set by :func:`launch_webserver`
        or :func:`connect_to_webserver`; otherwise ``None``.

    Examples
    --------
    >>> from ansys.fluent.core.rest.rest_session import RestSolverSession
    >>> session = RestSolverSession(
    ...     "http://127.0.0.1:54321",
    ...     auth_token="<token>",
    ... )
    >>> session.settings.setup.models.energy.enabled()
    True
    """

    def __init__(
        self,
        base_url: str,
        *,
        auth_token: str | None = None,
        component: str = "fluent_1",
        version: str = "",
        timeout: float = 30.0,
        max_retries: int = 0,
        retry_delay: float = 1.0,
    ) -> None:
        self._client = FluentRestClient(
            base_url,
            auth_token=auth_token,
            component=component,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )
        # Build the settings tree.  Retried a few times so transient startup
        # delays between port-open and auth-ready don't cause a hard failure.
        self._settings = self._build_settings_with_retry(version=version)

        # Connection metadata — set by launch_webserver / connect_to_webserver
        self.ip: str | None = None
        self.port: int | None = None
        self.auth_token: str | None = auth_token

        # Subprocess handle — set by launch_webserver when it starts Fluent
        self._process: subprocess.Popen | None = None

    def _build_settings_with_retry(
        self, version: str, retries: int = 5, delay: float = 2.0
    ):
        """Call get_root() with retries to handle transient 401s on startup.

        After ``_probe_server`` confirms the static-info endpoint responds,
        the
        ``/static-info`` endpoint usually also works.  In rare cases there is
        a short gap — this retry loop covers it.

        Parameters
        ----------
        version : str
            Passed through to :func:`get_root`.
        retries : int
            Total attempts before giving up.  Defaults to ``5``.
        delay : float
            Seconds to wait between attempts.  Defaults to ``2.0``.
        """
        for attempt in range(retries):
            try:
                return get_root(self._client, version=version)
            except Exception as exc:
                msg = str(exc)
                is_auth = (
                    "401" in msg
                    or "Unauthorized" in msg
                    or "Invalid password" in msg
                )
                if is_auth and attempt < retries - 1:
                    logger.debug(
                        "get_root attempt %d/%d failed (auth), retrying in %.1fs",
                        attempt + 1,
                        retries,
                        delay,
                    )
                    time.sleep(delay)
                    continue
                if is_auth:
                    raise RuntimeError(
                        "Server returned 401 Unauthorized — wrong token?\n"
                        "Set the token before calling launch_webserver():\n"
                        "  Python     : os.environ['FLUENT_WEBSERVER_TOKEN'] = '<token>'\n"
                        "  PowerShell : $Env:FLUENT_WEBSERVER_TOKEN = '<token>'"
                    ) from exc
                raise

    # -- Public properties -----------------------------------------------

    @property
    def client(self) -> FluentRestClient:
        """The underlying REST transport proxy."""
        return self._client

    @property
    def settings(self) -> "Group":
        """Root of the solver settings tree.

        Returns
        -------
        Group
            The root ``Group`` object whose children mirror the Fluent solver
            settings hierarchy.
        """
        return self._settings

    # -- Case file convenience methods -----------------------------------

    def read_case(self, file_name: str) -> None:
        """Read a Fluent case file via the REST settings tree.

        Delegates to ``settings.file.read_case(file_name=file_name)``, which
        issues ``POST /api/fluent_1/file/read-case`` with
        ``{"file_name": file_name}`` under the hood.

        Parameters
        ----------
        file_name : str
            Server-side path to the ``.cas`` or ``.cas.h5`` file.
        """
        logger.info("Reading case file: %s", file_name)
        self._settings.file.read_case(file_name=file_name)

    def read_case_data(self, file_name: str) -> None:
        """Read a Fluent case+data file via the REST settings tree.

        Delegates to ``settings.file.read_case_data(file_name=file_name)``,
        which issues ``POST /api/fluent_1/file/read-case-data`` with
        ``{"file_name": file_name}`` under the hood.

        Parameters
        ----------
        file_name : str
            Server-side path to the ``.cas`` or ``.cas.h5`` file.
        """
        logger.info("Reading case+data file: %s", file_name)
        self._settings.file.read_case_data(file_name=file_name)

    def read_data(self, file_name: str) -> None:
        """Read a Fluent data file via the REST settings tree.

        Delegates to ``settings.file.read_data(file_name=file_name)``, which
        issues ``POST /api/fluent_1/file/read-data`` with
        ``{"file_name": file_name}`` under the hood.

        Parameters
        ----------
        file_name : str
            Server-side path to the ``.dat`` or ``.dat.h5`` file.
        """
        logger.info("Reading data file: %s", file_name)
        self._settings.file.read_data(file_name=file_name)

    # -- Lifecycle -------------------------------------------------------

    def exit(self) -> None:
        """Terminate the attached Fluent process (if any) and clean up.

        If no subprocess is attached (e.g. when the session was created via
        :func:`connect_to_webserver`), this method is a no-op.
        """
        proc = self._process
        if proc is None:
            return
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        self._process = None

    def __enter__(self) -> "RestSolverSession":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.exit()
