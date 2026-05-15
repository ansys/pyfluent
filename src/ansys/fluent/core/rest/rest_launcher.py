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

"""Launch, connect, and session management for the Fluent REST transport.

This module provides the session class and two public launcher functions that
mirror PyFluent's ``launch_fluent`` / ``connect_to_fluent`` pattern for HTTP:

* :class:`RestSolverSession` – lightweight solver session that wires
  :class:`~ansys.fluent.core.rest.client.FluentRestClient` into
  :func:`~ansys.fluent.core.solver.flobject.get_root`.

* :func:`launch_webserver` – **primary entry point**.  Discovers a free local
  port, generates a secure random auth token, spawns the Fluent process with
  ``-ws -ws-port={port}``, waits until the embedded web server is reachable,
  and returns a fully connected :class:`RestSolverSession`.

* :func:`connect_to_webserver` – connects to an **already-running** web
  server.  Requires ``ip``, ``port``, and ``auth_token`` to be supplied
  explicitly.  Performs a reachability probe before returning the session.

Usage — launch (starts Fluent + SimBA locally)
----------------------------------------------
::

    from ansys.fluent.core.rest import launch_webserver

    session = launch_webserver()
    print(session.settings.setup.models.energy.enabled())
    session.exit()     # terminates the Fluent process

Usage — connect (SimBA already running)
----------------------------------------
::

    from ansys.fluent.core.rest import connect_to_webserver

    session = connect_to_webserver("127.0.0.1", 5000, auth_token="my-token")
    session.settings.setup.models.energy.enabled.set_state(False)
"""

from __future__ import annotations

import hashlib
import logging
import os
import secrets
import socket
import subprocess
import time
import urllib.error
import urllib.request

from ansys.fluent.core.launcher.process_launch_string import get_fluent_exe_path
from ansys.fluent.core.rest.client import FluentRestClient, FluentRestError
from ansys.fluent.core.solver.flobject import Group, get_root

__all__ = ["RestSolverSession", "connect_to_webserver", "launch_webserver"]

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_LOCALHOST = "127.0.0.1"
_SESSION_TOKEN: str | None = None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _get_free_port() -> int:
    """Return an available local TCP port using the OS ephemeral-port mechanism.

    Uses only the Python ``socket`` stdlib — no ANSYS-internal dependencies.

    Returns
    -------
    int
        A free TCP port number.

    Raises
    ------
    RuntimeError
        If the OS cannot bind to any port (extremely unlikely).
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("", 0))
            return sock.getsockname()[1]
    except OSError as exc:
        raise RuntimeError(
            "Could not find a free local TCP port. " f"OS error: {exc}"
        ) from exc


def _resolve_auth_token() -> str:
    """Return the session-cached auth token, generating it if needed.

    The token is a random 4-character hex string generated via
    :func:`secrets.token_hex`. It is cached at the module level for the
    lifetime of the Python process.

    Returns
    -------
    str
        The session auth token.
    """
    global _SESSION_TOKEN
    if _SESSION_TOKEN is None:
        _SESSION_TOKEN = secrets.token_hex(2)  # 4 hex chars
        logger.info("Generated session auth token (SHA-256 protected on wire).")
    return _SESSION_TOKEN


def _probe_server(
    base_url: str,
    auth_token: str,
    component: str = "fluent_1",
    timeout: float = 5.0,
) -> bool:
    """Return ``True`` if the SimBA server responds to an authenticated probe.

    Sends ``GET /api/{component}/static-info`` with the auth token.
    This matches the first authenticated settings call used by
    :class:`~ansys.fluent.core.rest.rest_session.RestSolverSession`.

    Parameters
    ----------
    base_url : str
        Root URL, e.g. ``"http://127.0.0.1:54321"``.
    auth_token : str
        Bearer token.
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"`` (solver).
        Use ``"fluent_meshing_1"`` for a meshing session.
    timeout : float, optional
        Socket timeout in seconds.  Defaults to ``5.0``.

    Returns
    -------
    bool
        ``True`` if the server returns any 2xx response.
    """
    url = f"{base_url}/api/{component}/static-info"
    req = urllib.request.Request(url, method="GET")
    req.add_header(
        "Authorization", f"Bearer {hashlib.sha256(auth_token.encode()).hexdigest()}"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout):  # nosec B310
            return True
    except Exception:
        return False


def _wait_for_server(port: int, timeout: int = 120, scheme: str = "http") -> None:
    """Block until the Fluent web server is fully ready.

    Two-phase check:

    * **Phase 1** — TCP connect: waits until the port is open (server process
      is listening).  Polls every 2 s.
    * **Phase 2** — Solver-ready probe: ``GET /api/connection/run_mode``.
      Returns as soon as the solver responds (any HTTP reply, including 401).
      A ``400 Fluent not running`` means the web-server is up but the solver
      is still initialising — keep waiting.  Polls every 3 s.

    Both phases share the same *timeout* deadline so the total wait never
    exceeds *timeout* seconds.

    Parameters
    ----------
    port : int
        TCP port to probe.
    timeout : int
        Maximum total seconds to wait.  Defaults to ``120``.
    scheme : str, optional
        URL scheme (``"http"`` or ``"https"``).  Defaults to ``"http"``.
        Must match the scheme used by :func:`launch_webserver`.

    Raises
    ------
    TimeoutError
        If the server is not ready within *timeout* seconds.
    """
    deadline = time.monotonic() + timeout

    # ── Phase 1: wait for TCP port to open ──────────────────────────────
    logger.info("[wait] Phase 1 — waiting for TCP port %d to open...", port)
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((_LOCALHOST, port), timeout=2.0):
                logger.info("[wait] Port %d is open.", port)
                break
        except OSError:
            time.sleep(2)
    else:
        raise TimeoutError(
            f"Fluent web server on port {port} did not open within {timeout}s."
        )

    # ── Phase 2: wait for solver to be ready (no 400) ───────────────────
    logger.info("[wait] Phase 2 — waiting for solver to be ready on port %d...", port)
    probe_url = f"{scheme}://{_LOCALHOST}:{port}/api/connection/run_mode"
    while time.monotonic() < deadline:
        try:
            req = urllib.request.Request(probe_url, method="GET")
            with urllib.request.urlopen(req, timeout=3):  # nosec B310
                logger.info("[wait] Solver is ready on port %d.", port)
                return
        except urllib.error.HTTPError as exc:
            if exc.code == 400:
                # Web server up but solver not initialised yet — keep waiting
                logger.debug("[wait] Solver not ready yet (400) — retrying...")
                time.sleep(3)
            elif exc.code == 401:
                # Auth required — server and solver are fully up
                logger.info("[wait] Solver ready (401 on probe) — proceeding.")
                return
            else:
                logger.debug("[wait] Unexpected HTTP %d — retrying...", exc.code)
                time.sleep(3)
        except Exception:
            time.sleep(3)

    raise TimeoutError(f"Fluent solver on port {port} not ready within {timeout}s.")


def _get_fluent_exe(
    product_version: str | None = None,
    fluent_path: str | None = None,
) -> str:
    """Resolve the Fluent executable path.

    Delegates to the existing PyFluent utility
    :func:`~ansys.fluent.core.launcher.process_launch_string.get_fluent_exe_path`
    which searches in order:

    1. *fluent_path* (user-supplied custom path)
    2. *product_version* → ``AWP_ROOTnnn`` env var
    3. ``PYFLUENT_FLUENT_ROOT`` env var
    4. Latest installed Fluent via ``AWP_ROOT*`` env vars

    Parameters
    ----------
    product_version : str, optional
        Fluent version string, e.g. ``"261"`` or ``"26.1.0"``.
    fluent_path : str, optional
        Explicit path to the Fluent executable.

    Returns
    -------
    str
        Absolute path to the Fluent executable.

    Raises
    ------
    FileNotFoundError
        If no Fluent installation can be found.
    """
    return str(
        get_fluent_exe_path(
            product_version=product_version,
            fluent_path=fluent_path,
        )
    )


# ---------------------------------------------------------------------------
# RestSolverSession
# ---------------------------------------------------------------------------


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
        IP address of the connected server.
    port : int | None
        Port of the connected server.
    auth_token : str | None
        Auth token used for the connection.

    Examples
    --------
    >>> from ansys.fluent.core.rest import RestSolverSession
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
        self._settings = self._build_settings_with_retry(version=version)
        self.ip: str | None = None
        self.port: int | None = None
        self.auth_token: str | None = auth_token
        self._process: subprocess.Popen | None = None

    def _build_settings_with_retry(
        self, version: str, retries: int = 5, delay: float = 2.0
    ):
        """Call ``get_root()`` with retries to handle transient 401s on startup.

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
            except FluentRestError as exc:
                is_auth = exc.status == 401
                if is_auth and attempt < retries - 1:
                    logger.debug(
                        "get_root attempt %d/%d failed (HTTP 401), retrying in %.1fs",
                        attempt + 1,
                        retries,
                        delay,
                    )
                    time.sleep(delay)
                    continue
                if is_auth:
                    raise RuntimeError(
                        "Server returned 401 Unauthorized — wrong token?"
                    ) from exc
                raise
            except Exception:
                raise

    @property
    def client(self) -> FluentRestClient:
        """The underlying REST transport proxy."""
        return self._client

    @property
    def settings(self) -> "Group":
        """Root of the solver settings tree."""
        return self._settings

    def read_case(self, file_name: str) -> None:
        """Read a Fluent case file via the REST settings tree.

        Parameters
        ----------
        file_name : str
            Server-side path to the ``.cas`` or ``.cas.h5`` file.
        """
        logger.info("Reading case file: %s", file_name)
        self._settings.file.read_case(file_name=file_name)

    def read_case_data(self, file_name: str) -> None:
        """Read a Fluent case+data file via the REST settings tree.

        Parameters
        ----------
        file_name : str
            Server-side path to the ``.cas`` or ``.cas.h5`` file.
        """
        logger.info("Reading case+data file: %s", file_name)
        self._settings.file.read_case_data(file_name=file_name)

    def read_data(self, file_name: str) -> None:
        """Read a Fluent data file via the REST settings tree.

        Parameters
        ----------
        file_name : str
            Server-side path to the ``.dat`` or ``.dat.h5`` file.
        """
        logger.info("Reading data file: %s", file_name)
        self._settings.file.read_data(file_name=file_name)

    def exit(self) -> None:
        """Terminate the attached Fluent process (if any) and clean up."""
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
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        self.exit()


# ---------------------------------------------------------------------------
# Public API — launchers
# ---------------------------------------------------------------------------


def launch_webserver(
    *,
    product_version: str | None = None,
    fluent_path: str | None = None,
    dimension: str = "3ddp",
    start_timeout: int = 60,
    scheme: str = "http",
    component: str = "fluent_1",
    version: str = "261",
    timeout: float = 30.0,
    max_retries: int = 0,
    retry_delay: float = 1.0,
) -> RestSolverSession:
    """Launch a local Fluent process with the SimBA web server enabled.

    This is the **primary entry point** for using the REST transport layer.
    It mirrors :func:`ansys.fluent.core.launcher.launcher.launch_fluent` for
    the HTTP transport.

    The function performs the following steps automatically:

    1. Generates a secure, random auth token for the session.
    2. Discovers a free local TCP port using the Python ``socket`` stdlib.
    3. Resolves the Fluent executable (via *fluent_path*, *product_version*,
       or the ``AWP_ROOT*`` / ``PYFLUENT_FLUENT_ROOT`` env vars).
    4. Spawns Fluent with ``-ws -ws-port={port}`` and injects the
       auth token into the subprocess environment.
    5. Polls ``http://localhost:{port}/`` until the server responds or
       *start_timeout* expires (raises :class:`TimeoutError`).
    6. Calls :func:`connect_to_webserver` to build a
       :class:`~ansys.fluent.core.rest.rest_session.RestSolverSession`.
    7. Attaches the subprocess handle so :meth:`RestSolverSession.exit`
       terminates Fluent.

    Parameters
    ----------
    product_version : str, optional
        Fluent version string, e.g. ``"261"`` or ``"26.1.0"``.  Used to
        locate the Fluent executable via ``AWP_ROOTnnn``.  If omitted, the
        latest installed version is used automatically.
    fluent_path : str, optional
        Explicit path to the Fluent executable.  Takes precedence over
        *product_version* and all environment variables.
    dimension : str, optional
        Fluent solver dimension argument.  Defaults to ``"3ddp"``
        (3-D double precision).
    start_timeout : int, optional
        Maximum seconds to wait for the web server to become reachable.
        Defaults to ``60``.
    scheme : str, optional
        URL scheme (``"http"`` or ``"https"``).  Defaults to ``"http"``.
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"`` (solver).
    version : str, optional
        Fluent version string passed to
        :func:`~ansys.fluent.core.solver.flobject.get_root` for code-
        generated settings.  Defaults to ``"261"``.
    timeout : float, optional
        HTTP socket timeout in seconds for every REST request.  Defaults
        to ``30.0``.
    max_retries : int, optional
        Maximum automatic retries on transient HTTP errors.  Defaults to
        ``0``.
    retry_delay : float, optional
        Base delay in seconds between retries (exponential back-off).
        Defaults to ``1.0``.

    Returns
    -------
    RestSolverSession
        A fully initialised solver session whose settings tree communicates
        over HTTP.  The session exposes:

        * ``session.ip`` — ``"127.0.0.1"``
        * ``session.port`` — the auto-discovered port
        * ``session.auth_token`` — the auto-generated token
        * ``session.exit()`` — terminates the Fluent process

    Raises
    ------
    RuntimeError
        If no free TCP port can be found.
    FileNotFoundError
        If the Fluent executable cannot be located.
    ValueError
        If *scheme* is not ``"http"`` or ``"https"``.
    TimeoutError
        If the web server does not start within *start_timeout* seconds.
    ConnectionError
        If the reachability probe in :func:`connect_to_webserver` fails
        after the server appeared ready.

    Examples
    --------
    >>> from ansys.fluent.core.rest import launch_webserver
    >>> session = launch_webserver()
    >>> session.settings.setup.models.energy.enabled()
    True
    >>> session.exit()
    """
    if scheme not in ("http", "https"):
        raise ValueError(f"scheme must be 'http' or 'https', got {scheme!r}")

    # 1 — generate auth token
    auth_token = _resolve_auth_token()

    # 2 — discover a free local TCP port (pure stdlib)
    port = _get_free_port()
    logger.info("Discovered free port %d for Fluent web server.", port)

    # 3 — resolve the Fluent executable
    fluent_exe = _get_fluent_exe(
        product_version=product_version,
        fluent_path=fluent_path,
    )

    # 4 — build the launch command and spawn Fluent
    launch_cmd = [fluent_exe, dimension, "-ws", f"-ws-port={port}"]
    logger.info("Launching Fluent: %s", launch_cmd)

    env = os.environ.copy()
    env["FLUENT_WEBSERVER_TOKEN"] = auth_token
    process = subprocess.Popen(launch_cmd, env=env)  # nosec B603 B607

    if process.poll() is not None:
        raise RuntimeError(
            f"Fluent process exited immediately with return code "
            f"{process.returncode}. Command: {launch_cmd}"
        )
    # Wait for the server to become reachable
    _wait_for_server(port, timeout=start_timeout, scheme=scheme)

    # 5 — build session (Fluent web server starting in background — no blocking wait)
    base_url = f"{scheme}://{_LOCALHOST}:{port}"
    session = RestSolverSession(
        base_url,
        auth_token=auth_token,
        component=component,
        version=version,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
    )
    session.ip = _LOCALHOST
    session.port = port
    session.auth_token = auth_token

    # 6 — attach the subprocess so session.exit() terminates Fluent
    session._process = process

    return session


def connect_to_webserver(
    ip: str,
    port: int,
    auth_token: str,
    *,
    scheme: str = "http",
    component: str = "fluent_1",
    version: str = "261",
    timeout: float = 30.0,
    max_retries: int = 0,
    retry_delay: float = 1.0,
) -> RestSolverSession:
    """Connect to an already-running Fluent REST (SimBA) server.

    Use this function when the SimBA server is already running and you know
    its ``ip``, ``port``, and ``auth_token``.  For a fully automated local
    launch use :func:`launch_webserver` instead.

    Parameters
    ----------
    ip : str
        IP address or hostname of the SimBA server, e.g. ``"127.0.0.1"``.
    port : int
        TCP port the SimBA server is listening on.
    auth_token : str
        Bearer token (password) for authentication.
    scheme : str, optional
        URL scheme.  Must be ``"http"`` or ``"https"``.  Defaults to
        ``"http"``.
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"`` (solver).
    version : str, optional
        Fluent version string (e.g. ``"261"``).  Defaults to ``"261"``.
    timeout : float, optional
        HTTP socket timeout in seconds.  Defaults to ``30.0``.
    max_retries : int, optional
        Maximum automatic retries on transient HTTP errors.  Defaults to
        ``0``.
    retry_delay : float, optional
        Base delay in seconds between retries (exponential back-off).
        Defaults to ``1.0``.

    Returns
    -------
    RestSolverSession
        A fully initialised solver session with ``ip``, ``port``, and
        ``auth_token`` attributes set.

    Raises
    ------
    ValueError
        If *scheme* is not ``"http"`` or ``"https"``.
    ConnectionError
        If the server does not respond to the reachability probe.

    Examples
    --------
    >>> from ansys.fluent.core.rest import connect_to_webserver
    >>> session = connect_to_webserver(
    ...     ip="127.0.0.1",
    ...     port=5000,
    ...     auth_token="my-secret-token",
    ... )
    >>> session.settings.setup.models.energy.enabled()
    True
    """
    if scheme not in ("http", "https"):
        raise ValueError(f"scheme must be 'http' or 'https', got {scheme!r}")

    base_url = f"{scheme}://{ip}:{port}"

    # Reachability probe — fail-fast before building the settings tree
    if not _probe_server(base_url, auth_token, timeout=min(timeout, 5.0)):
        raise ConnectionError(
            f"SimBA server at {base_url} did not respond to the reachability "
            f"probe (GET /api/{component}/static-info). "
            "Verify that the server is running on the given ip and port, "
            "and that the auth_token is correct."
        )

    session = RestSolverSession(
        base_url,
        auth_token=auth_token,
        component=component,
        version=version,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
    )
    session.ip = ip
    session.port = port
    session.auth_token = auth_token
    return session
