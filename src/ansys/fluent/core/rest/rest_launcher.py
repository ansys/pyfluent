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

This module provides a **standalone, low-level** REST transport layer.
It does **not** build a settings tree (no ``session.settings``), expose
convenience helpers like ``read_case()``, or depend on ``flobject``.
All interaction is via explicit path-based calls (``get_var``, ``set_var``,
``execute_command``, etc.).

Transport security
~~~~~~~~~~~~~~~~~~
``launch_webserver()`` uses **HTTPS** when user-provided TLS certificates
are found (via the ``cert_dir`` parameter, the
``FLUENT_WEBSERVER_CERTIFICATE_ROOT`` environment variable, or the default
Fluent install path).  Falls back to plain HTTP if no certificates are
available.

Public API
----------
* :func:`launch_webserver` — spawn Fluent with ``-ws``, returning a connected
   :class:`~ansys.fluent.core.rest.client.FluentRestClient`.

Examples
--------
Launch a local Fluent web server and connect with a REST client::

     from ansys.fluent.core.rest import launch_webserver
     client = launch_webserver()
     client.get_var("setup/models/energy/enabled")
"""

from __future__ import annotations

import logging
import os
import secrets
import socket
import ssl
import subprocess
import time
import urllib.error
import urllib.request

from ansys.fluent.core.launcher.process_launch_string import get_fluent_exe_path
from ansys.fluent.core.rest.client import FluentRestClient
from ansys.fluent.core.rest.tls import _build_ssl_context, _find_cert_dir

__all__ = ["launch_webserver"]

logger = logging.getLogger(__name__)

_LOCALHOST = "127.0.0.1"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _get_free_port() -> int:
    """Return an available local TCP port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((_LOCALHOST, 0))
            return sock.getsockname()[1]
    except OSError as exc:
        raise RuntimeError(f"No free TCP port: {exc}") from exc


def _generate_auth_token(nbytes: int = 32) -> str:
    """Generate a cryptographically secure URL-safe auth token.

    Returns
    -------
    str
        A URL-safe base-64 token (43 chars for the default 32 bytes).
    """
    token = secrets.token_urlsafe(nbytes)
    logger.debug("Generated per-launch auth token.")
    return token


def _wait_for_port(port: int, deadline: float) -> None:
    """Block until *port* accepts TCP connections (Phase 1)."""
    logger.info("[wait] Phase 1 — waiting for TCP port %d to open...", port)
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((_LOCALHOST, port), timeout=2.0):
                logger.info("[wait] Port %d is open.", port)
                return
        except OSError:
            time.sleep(2)
    raise TimeoutError(f"Port {port} not open in time.")


def _wait_for_solver_ready(
    probe_url: str,
    ssl_context: ssl.SSLContext | None,
    deadline: float,
) -> None:
    """Block until the solver answers the readiness probe (Phase 2)."""
    logger.info("[wait] Phase 2 — waiting for solver to be ready...")
    while time.monotonic() < deadline:
        try:
            req = urllib.request.Request(probe_url, method="GET")
            with urllib.request.urlopen(
                req, timeout=3, context=ssl_context
            ):  # nosec B310
                logger.info("[wait] Solver is ready.")
                return
        except urllib.error.HTTPError as exc:
            if exc.code == 401:
                # Auth required — server and solver are fully up.
                logger.info("[wait] Solver ready (HTTP 401 on probe) — proceeding.")
                return
            # 400 = solver still initialising; anything else = transient.
            logger.debug(
                "[wait] Solver not ready yet (HTTP %d) — retrying...", exc.code
            )
            time.sleep(3)
        except (urllib.error.URLError, OSError):
            # Connection refused / reset / DNS failure — not listening yet.
            time.sleep(3)
    raise TimeoutError("Solver not ready in time.")


def _wait_for_server(
    port: int,
    timeout: int = 120,
    ssl_context: ssl.SSLContext | None = None,
) -> None:
    """Block until the Fluent web server is ready (port open, then solver up)."""
    deadline = time.monotonic() + timeout
    scheme = "https" if ssl_context else "http"
    probe_url = f"{scheme}://{_LOCALHOST}:{port}/api/connection/run_mode"

    _wait_for_port(port, deadline)
    _wait_for_solver_ready(probe_url, ssl_context, deadline)


def _resolve_transport_security(
    cert_dir: str | None,
) -> tuple[str | None, ssl.SSLContext | None]:
    """Return ``(cert_dir, ssl_context)`` for HTTPS, or ``(None, None)`` for HTTP."""
    resolved_cert_dir = _find_cert_dir(cert_dir)
    if resolved_cert_dir:
        ssl_ctx = _build_ssl_context(resolved_cert_dir)
        logger.info("HTTPS enabled — certificates from %s", resolved_cert_dir)
        return resolved_cert_dir, ssl_ctx

    logger.warning(
        "No TLS certificates found. Launching Fluent in HTTP mode. "
        "For HTTPS, provide webserver.crt, webserver.key, and dh.pem."
    )
    return None, None


def _spawn_fluent(
    fluent_exe: str,
    dimension: str,
    port: int,
    auth_token: str,
    cert_dir: str | None,
) -> subprocess.Popen:
    """Spawn the Fluent web server process; raise if it exits immediately."""
    launch_cmd = [fluent_exe, dimension, "-ws", f"-ws-port={port}"]
    logger.info("Launching Fluent: %s", launch_cmd)

    env = os.environ.copy()
    env["FLUENT_WEBSERVER_TOKEN"] = auth_token
    if cert_dir:
        env["FLUENT_WEBSERVER_CERTIFICATE_ROOT"] = cert_dir

    process = subprocess.Popen(launch_cmd, env=env)  # nosec B603 B607
    if process.poll() is not None:
        raise RuntimeError(f"Fluent exited immediately (rc={process.returncode}).")
    return process


def _connect_client(
    port: int,
    ssl_context: ssl.SSLContext | None,
    auth_token: str,
    component: str,
    timeout: float,
    max_retries: int,
    retry_delay: float,
) -> FluentRestClient:
    """Build a :class:`FluentRestClient` bound to the running server."""
    scheme = "https" if ssl_context else "http"
    base_url = f"{scheme}://{_LOCALHOST}:{port}"
    return FluentRestClient(
        base_url,
        auth_token=auth_token,
        component=component,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        ssl_context=ssl_context,
    )


def _terminate_process(process: subprocess.Popen) -> None:
    """Terminate a process, escalating to ``kill`` if it does not exit."""
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


# ---------------------------------------------------------------------------
# Public API — launchers
# ---------------------------------------------------------------------------


def launch_webserver(
    *,
    product_version: str | None = None,
    fluent_path: str | None = None,
    cert_dir: str | None = None,
    dimension: str = "3ddp",
    start_timeout: int = 60,
    component: str = "fluent_1",
    timeout: float = 30.0,
    max_retries: int = 0,
    retry_delay: float = 1.0,
) -> FluentRestClient:
    """Launch a local Fluent process with the embedded web server.

    Discovers user-provided TLS certificates and launches Fluent with
    HTTPS when found, otherwise falls back to plain HTTP.

    Parameters
    ----------
    product_version : str, optional
        Fluent version, e.g. ``"261"``.
    fluent_path : str, optional
        Explicit path to the Fluent executable.
    cert_dir : str, optional
        Path to a directory containing ``webserver.crt``,
        ``webserver.key``, and ``dh.pem``.  Takes precedence over the
        ``FLUENT_WEBSERVER_CERTIFICATE_ROOT`` environment variable and
        the default Fluent install path.  If no certificates are found
        from any source, Fluent starts in HTTP mode.
    dimension : str, optional
        Solver dimension.  Defaults to ``"3ddp"``.
    start_timeout : int, optional
        Max seconds to wait for the server.  Defaults to ``60``.
    component : str, optional
        DataModel component.  Defaults to ``"fluent_1"``.
    timeout : float, optional
        HTTP timeout in seconds.  Defaults to ``30.0``.
    max_retries : int, optional
        Retries on transient errors.  Defaults to ``0``.
    retry_delay : float, optional
        Base retry delay in seconds.  Defaults to ``1.0``.

    Returns
    -------
    FluentRestClient

    Raises
    ------
    RuntimeError
        If the Fluent process exits immediately after spawning.
    FileNotFoundError
        If the Fluent executable cannot be located.
    TimeoutError
        If the web server does not start within *start_timeout* seconds.
    Exception
        Any exception during server connection is re-raised after
        terminating the spawned process.
    """
    # 1 — generate a fresh per-launch auth token
    auth_token = _generate_auth_token()

    # 2 — discover user-provided TLS certificates
    resolved_cert_dir, ssl_ctx = _resolve_transport_security(cert_dir)

    # 3 — discover a free local TCP port (pure stdlib)
    port = _get_free_port()
    logger.info("Discovered free port %d for Fluent web server.", port)

    # 4 — resolve the Fluent executable
    fluent_exe = str(
        get_fluent_exe_path(product_version=product_version, fluent_path=fluent_path)
    )

    # 5 — build the launch command and spawn Fluent
    process = _spawn_fluent(fluent_exe, dimension, port, auth_token, resolved_cert_dir)

    # 6 — wait for the web server and construct the session
    try:
        _wait_for_server(port, timeout=start_timeout, ssl_context=ssl_ctx)
        return _connect_client(
            port=port,
            ssl_context=ssl_ctx,
            auth_token=auth_token,
            component=component,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )
    except Exception:
        logger.exception(
            "Failed after launching Fluent (pid=%d) — terminating.", process.pid
        )
        _terminate_process(process)
        raise
