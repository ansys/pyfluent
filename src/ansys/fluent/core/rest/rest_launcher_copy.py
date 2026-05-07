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

"""Launch and connect to a Fluent REST (SimBA) web server.

This module provides two public functions that mirror PyFluent's
``launch_fluent`` / ``connect_to_fluent`` pattern for the HTTP transport:

* :func:`launch_webserver` – **primary entry point**.  Discovers a free local
  port, reads the ``FLUENT_WEBSERVER_TOKEN`` environment variable, spawns the
  Fluent process with ``-ws -ws-port={port}``, waits until the embedded SimBA
  server is reachable, and returns a fully connected
  :class:`~ansys.fluent.core.rest.rest_session.RestSolverSession`.

* :func:`connect_to_webserver` – connects to an **already-running** SimBA
  server.  Requires ``ip``, ``port``, and ``auth_token`` to be supplied
  explicitly.  Performs a reachability probe before returning the session.

Environment variables
---------------------
``FLUENT_WEBSERVER_TOKEN``
    Bearer token (password) that the embedded SimBA server expects.
    **Required** — set this variable before calling :func:`launch_webserver`.

Usage — launch (starts Fluent + SimBA locally)
----------------------------------------------
::

    # 1. Set the token in your shell:
    #    export FLUENT_WEBSERVER_TOKEN=my-secret-token      (Linux/macOS)
    #    $Env:FLUENT_WEBSERVER_TOKEN = 'my-secret-token'    (PowerShell)

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

import logging
import os
import socket
import subprocess
import time
import urllib.error
import urllib.request

from ansys.fluent.core.launcher.process_launch_string import get_fluent_exe_path
from ansys.fluent.core.rest.rest_session import RestSolverSession

__all__ = ["connect_to_webserver", "launch_webserver"]

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_LOCALHOST = "127.0.0.1"
_TOKEN_ENV_VAR = "FLUENT_WEBSERVER_TOKEN"


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
            "Could not find a free local TCP port. "
            f"OS error: {exc}"
        ) from exc


def _read_auth_token() -> str:
    """Read the mandatory auth token from ``FLUENT_WEBSERVER_TOKEN``.

    Returns
    -------
    str
        The value of ``FLUENT_WEBSERVER_TOKEN``.

    Raises
    ------
    RuntimeError
        If ``FLUENT_WEBSERVER_TOKEN`` is not set or is empty.
    """
    token = os.environ.get(_TOKEN_ENV_VAR)
    if not token:
        raise RuntimeError(
            f"Environment variable '{_TOKEN_ENV_VAR}' is not set. "
            "Set it to the Bearer token (password) for the SimBA web server "
            "before calling launch_webserver().\n"
            "Example (Linux/macOS):\n"
            f"    export {_TOKEN_ENV_VAR}=my-secret-token\n"
            "Example (Windows PowerShell):\n"
            f"    $Env:{_TOKEN_ENV_VAR} = 'my-secret-token'"
        )
    return token


def _probe_server(base_url: str, auth_token: str, timeout: float = 5.0) -> bool:
    """Return ``True`` if the SimBA server responds to a lightweight probe.

    Sends ``GET /api/connection/run_mode`` with the auth token.

    Parameters
    ----------
    base_url : str
        Root URL, e.g. ``"http://127.0.0.1:54321"``.
    auth_token : str
        Bearer token.
    timeout : float, optional
        Socket timeout in seconds.  Defaults to ``5.0``.

    Returns
    -------
    bool
        ``True`` if the server returns any 2xx response.
    """
def _probe_server(base_url: str, auth_token: str, timeout: float = 5.0) -> bool:
    """Return ``True`` if the SimBA server responds to an authenticated probe.

    Sends ``GET /api/fluent_1/static-info`` with the auth token — the same
    endpoint that get_static_info() uses, so we confirm auth works.
    """
    url = f"{base_url}/api/fluent_1/static-info"
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {auth_token}")
    try:
        with urllib.request.urlopen(req, timeout=timeout):
            return True
    except Exception:
        return False


def _wait_for_server(port: int, auth_token: str, timeout: int = 60) -> None:
    """Block until the SimBA server at *port* responds, or raise on timeout.

    Uses :func:`_probe_server` (authenticated ``GET /api/connection/run_mode``)
    to check readiness, polling every second.

    Parameters
    ----------
    port : int
        Local TCP port the Fluent web server should be listening on.
    auth_token : str
        Bearer token used for the authenticated readiness probe.
    timeout : int, optional
        Maximum seconds to wait.  Defaults to ``60``.

    Raises
    ------
    TimeoutError
        If the server does not respond within *timeout* seconds.
    """
    base_url = f"http://{_LOCALHOST}:{port}"
    start = time.time()
    while time.time() - start < timeout:
        if _probe_server(base_url, auth_token, timeout=2.0):
            logger.info("Fluent web server is ready on port %d.", port)
            return
        time.sleep(1)
    raise TimeoutError(
        f"Fluent web server on port {port} did not start within {timeout}s."
    )


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
# Public API
# ---------------------------------------------------------------------------


def launch_webserver(
    *,
    product_version: str | None = None,
    fluent_path: str | None = None,
    dimension: str = "3ddp",
    start_timeout: int = 60,
    scheme: str = "http",
    component: str = "fluent_1",
    version: str = "",
    timeout: float = 30.0,
    max_retries: int = 0,
    retry_delay: float = 1.0,
) -> RestSolverSession:
    """Launch a local Fluent process with the SimBA web server enabled.

    This is the **primary entry point** for using the REST transport layer.
    It mirrors :func:`ansys.fluent.core.launcher.launcher.launch_fluent` for
    the HTTP transport.

    The function performs the following steps automatically:

    1. Reads the mandatory auth token from the ``FLUENT_WEBSERVER_TOKEN``
       environment variable (raises :class:`RuntimeError` if unset).
    2. Discovers a free local TCP port using the Python ``socket`` stdlib.
    3. Resolves the Fluent executable (via *fluent_path*, *product_version*,
       or the ``AWP_ROOT*`` / ``PYFLUENT_FLUENT_ROOT`` env vars).
    4. Spawns Fluent with ``-ws -ws-port={port}`` and injects
       ``FLUENT_WEBSERVER_TOKEN`` into the subprocess environment.
    5. Polls ``http://localhost:{port}/`` until the server responds or
       *start_timeout* expires (raises :class:`TimeoutError`).
    6. Calls :func:`connect_to_webserver` to build a
       :class:`~ansys.fluent.core.rest.rest_session.RestSolverSession`.
    7. Attaches the subprocess handle so :meth:`RestSolverSession.exit`
       terminates Fluent.

    .. note::

        Before calling this function you **must** set the environment
        variable::

            export FLUENT_WEBSERVER_TOKEN=<token>     # Linux / macOS
            $Env:FLUENT_WEBSERVER_TOKEN = '<token>'   # Windows PowerShell

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
        generated settings.
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
        * ``session.auth_token`` — the token from the environment
        * ``session.exit()`` — terminates the Fluent process

    Raises
    ------
    RuntimeError
        If ``FLUENT_WEBSERVER_TOKEN`` is not set, or if no free TCP port
        can be found.
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
    >>> import os
    >>> os.environ["FLUENT_WEBSERVER_TOKEN"] = "my-secret-token"
    >>> from ansys.fluent.core.rest import launch_webserver
    >>> session = launch_webserver()
    >>> session.settings.setup.models.energy.enabled()
    True
    >>> session.exit()
    """
    if scheme not in ("http", "https"):
        raise ValueError(f"scheme must be 'http' or 'https', got {scheme!r}")

    # 1 — mandatory auth token from environment
    auth_token = _read_auth_token()

    # 2 — discover a free local TCP port (pure stdlib)
    port = _get_free_port()
    logger.info("Discovered free port %d for Fluent web server.", port)

    # 3 — resolve the Fluent executable
    fluent_exe = _get_fluent_exe(
        product_version=product_version,
        fluent_path=fluent_path,
    )

    # 4 — build the launch command and spawn Fluent
    launch_cmd = f'"{fluent_exe}" {dimension} -ws -ws-port={port}'
    logger.info("Launching Fluent: %s", launch_cmd)

    env = os.environ.copy()
    env[_TOKEN_ENV_VAR] = auth_token
    process = subprocess.Popen(launch_cmd, env=env)  # nosec B603

    if process.poll() is not None:
        raise RuntimeError(
            f"Fluent process exited immediately with return code "
            f"{process.returncode}. Command: {launch_cmd}"
        )

    # 5 — wait for the web server to become reachable
    try:
        _wait_for_server(port, auth_token, timeout=start_timeout)
    except TimeoutError:
        process.terminate()
        raise

    # 6 — connect via the normal connect_to_webserver path
    session = connect_to_webserver(
        ip=_LOCALHOST,
        port=port,
        auth_token=auth_token,
        scheme=scheme,
        component=component,
        version=version,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
    )

    # 7 — attach the subprocess so session.exit() terminates Fluent
    session._process = process

    return session


def connect_to_webserver(
    ip: str,
    port: int,
    auth_token: str,
    *,
    scheme: str = "http",
    component: str = "fluent_1",
    version: str = "",
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
        Fluent version string (e.g. ``"261"``).
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
            "probe (GET /api/connection/run_mode). "
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
