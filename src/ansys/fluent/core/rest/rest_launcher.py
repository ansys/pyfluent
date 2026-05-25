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
``launch_webserver()`` always uses **HTTPS** with auto-generated ephemeral
TLS certificates.  ``connect_to_webserver()`` uses HTTPS when a ``ca_cert``
is provided, otherwise plain HTTP.

Public API
----------
* :class:`RestSolverSession` — thin wrapper around :class:`FluentRestClient`.
* :func:`launch_webserver` — spawn Fluent with ``-ws``, return a session.
* :func:`connect_to_webserver` — connect to a running web server.

Examples
--------
Launch a local Fluent web server and connect with a REST session::

    from ansys.fluent.core.rest import launch_webserver, connect_to_webserver
    session = launch_webserver()
    session.get_var("setup/models/energy/enabled")
    session.exit()

Connect to an already-running web server with known IP, port, and auth token::

    session = connect_to_webserver("127.0.0.1", <port>, auth_token=<auth_token>)
    session.set_var("setup/models/energy/enabled", False)
"""

from __future__ import annotations

import hashlib
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
from ansys.fluent.core.rest.tls import _TlsCertificateManager

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


def _probe_server(
    base_url: str,
    auth_token: str,
    component: str = "fluent_1",
    timeout: float = 5.0,
    ssl_context: ssl.SSLContext | None = None,
) -> bool:
    """Return ``True`` if the server responds to an auth probe."""
    url = f"{base_url}/api/{component}/static-info"
    req = urllib.request.Request(url, method="HEAD")
    req.add_header(
        "Authorization", f"Bearer {hashlib.sha256(auth_token.encode()).hexdigest()}"
    )
    try:
        with urllib.request.urlopen(
            req, timeout=timeout, context=ssl_context
        ):  # nosec B310
            return True
    except Exception:
        return False


def _wait_for_server(
    port: int,
    timeout: int = 120,
    ssl_context: ssl.SSLContext | None = None,
) -> None:
    """Block until the Fluent web server is fully ready.

    Phase 1: TCP connect (port open).  Phase 2: HTTP probe (solver ready).
    Raises :class:`TimeoutError` if not ready within *timeout* seconds.
    """
    scheme = "https" if ssl_context else "http"
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
        raise TimeoutError(f"Port {port} not open within {timeout}s.")

    # ── Phase 2: wait for solver to be ready (no 400) ───────────────────
    logger.info("[wait] Phase 2 — waiting for solver to be ready on port %d...", port)
    probe_url = f"{scheme}://{_LOCALHOST}:{port}/api/connection/run_mode"
    while time.monotonic() < deadline:
        try:
            req = urllib.request.Request(probe_url, method="GET")
            with urllib.request.urlopen(
                req, timeout=3, context=ssl_context
            ):  # nosec B310
                logger.info("[wait] Solver is ready on port %d.", port)
                return
        except urllib.error.HTTPError as exc:
            if exc.code == 400:
                # Web server is up but solver has not initialised yet
                logger.debug("[wait] Solver not ready yet (HTTP 400) — retrying...")
                time.sleep(3)
            elif exc.code == 401:
                # Auth required — server and solver are fully up
                logger.info("[wait] Solver ready (HTTP 401 on probe) — proceeding.")
                return
            else:
                logger.debug("[wait] Unexpected HTTP %d — retrying...", exc.code)
                time.sleep(3)
        except urllib.error.URLError:
            # Connection refused / DNS failure — server not yet listening
            time.sleep(3)
        except OSError:
            # Low-level socket error (e.g. connection reset)
            time.sleep(3)

    raise TimeoutError(f"Solver on port {port} not ready within {timeout}s.")


def _get_fluent_exe(
    product_version: str | None = None,
    fluent_path: str | None = None,
) -> str:
    """Resolve the Fluent executable path via :func:`get_fluent_exe_path`."""
    return str(
        get_fluent_exe_path(
            product_version=product_version,
            fluent_path=fluent_path,
        )
    )


# ---------------------------------------------------------------------------
# Public API — launchers
# ---------------------------------------------------------------------------


def launch_webserver(
    *,
    product_version: str | None = None,
    fluent_path: str | None = None,
    dimension: str = "3ddp",
    start_timeout: int = 60,
    component: str = "fluent_1",
    timeout: float = 30.0,
    max_retries: int = 0,
    retry_delay: float = 1.0,
) -> FluentRestClient:
    """Launch a local Fluent process with the embedded HTTPS web server.

    Auto-generates TLS certs and auth token, discovers a free port,
    spawns Fluent with ``-ws``, and returns a connected session.

    Parameters
    ----------
    product_version : str, optional
        Fluent version, e.g. ``"261"``.
    fluent_path : str, optional
        Explicit path to the Fluent executable.
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
        terminating the spawned process and cleaning up TLS files.
    """
    # 1 — generate a fresh per-launch auth token
    auth_token = _generate_auth_token()

    # 2 — generate ephemeral TLS certificates (lifecycle managed by _TlsCertificateManager)
    tls = _TlsCertificateManager()
    tls.generate()
    ssl_ctx = tls.ssl_context

    # 3 — discover a free local TCP port (pure stdlib)
    port = _get_free_port()
    logger.info("Discovered free port %d for Fluent web server.", port)

    # 4 — resolve the Fluent executable
    fluent_exe = _get_fluent_exe(
        product_version=product_version,
        fluent_path=fluent_path,
    )

    # 5 — build the launch command and spawn Fluent
    launch_cmd = [fluent_exe, dimension, "-ws", f"-ws-port={port}"]
    logger.info("Launching Fluent: %s", launch_cmd)

    env = os.environ.copy()
    env["FLUENT_WEBSERVER_TOKEN"] = auth_token
    env["FLUENT_WEBSERVER_CERTIFICATE_ROOT"] = tls.cert_dir
    process = subprocess.Popen(launch_cmd, env=env)  # nosec B603 B607

    if process.poll() is not None:
        tls.cleanup()
        raise RuntimeError(f"Fluent exited immediately (rc={process.returncode}).")

    # 6 — wait for the web server and construct the session
    # Wrap post-Popen work in try/except so a failure (timeout,
    # auth error, etc.) terminates the spawned process before re-raising.
    try:
        _wait_for_server(port, timeout=start_timeout, ssl_context=ssl_ctx)

        scheme = "https" if ssl_ctx else "http"
        base_url = f"{scheme}://{_LOCALHOST}:{port}"
        session = FluentRestClient(
            base_url,
            auth_token=auth_token,
            component=component,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            ssl_context=ssl_ctx,
        )
    except Exception:
        logger.exception(
            "Failed after launching Fluent (pid=%d) — terminating process.",
            process.pid,
        )
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        tls.cleanup()
        raise

    return session
