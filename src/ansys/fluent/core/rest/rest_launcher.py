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
When connecting to a server via ``connect_to_webserver()``, TLS (HTTPS) is supported
if the server is configured with the appropriate certificates.

Public API
----------
* :class:`RestSolverSession` — session wrapper for the low-level REST client.
* :func:`connect_to_webserver` — connect to an already-running Fluent REST server,
   returning a :class:`RestSolverSession`.

Examples
--------
Connect to an already-running Fluent web server and interact via the REST client::

     from ansys.fluent.core.rest import connect_to_webserver
     session = connect_to_webserver(
         ip="127.0.0.1",
         port=5000,
         auth_token="my-secret-token",
     )
     client = session._client
     enabled = client.get_var("setup/models/energy/enabled")
"""

from __future__ import annotations

import hashlib
import logging
import ssl
import urllib.error
import urllib.request

from ansys.fluent.core.rest.client import FluentRestClient

__all__ = ["connect_to_webserver", "RestSolverSession"]

logger = logging.getLogger(__name__)


def _get_ssl_context_for_https() -> ssl.SSLContext | None:
    """Discover and build SSL context for HTTPS connections.

    Searches for certificates in the following order:
    1. ``FLUENT_WEBSERVER_CERTIFICATE_ROOT`` environment variable
    2. Default Fluent installation path via ``AWP_ROOTnnn``

    Required files at the certificate directory:
    * ``webserver.crt`` — SSL certificate
    * ``webserver.key`` — private key
    * ``dh.pem`` — DH parameters

    Returns
    -------
    ssl.SSLContext or None
        An SSL context configured with the discovered certificates, or ``None``
        if no valid certificate directory was found.
    """
    try:
        from ansys.fluent.core.rest.tls import _build_ssl_context, _find_cert_dir

        cert_dir = _find_cert_dir()
        if cert_dir:
            return _build_ssl_context(cert_dir)
    except Exception as exc:
        logger.debug("Failed to build SSL context: %s", exc)
    return None


def _probe_server(
    base_url: str,
    auth_token: str | None,
    timeout: float,
    ssl_context: ssl.SSLContext | None = None,
) -> bool:
    """Check if a Fluent REST server is reachable via the readiness probe endpoint.

    Sends a GET request to ``/api/connection/run_mode`` and returns ``True`` if the
    server responds with a 2xx status code or 401 (Unauthorized, which indicates
    the server is up and auth is required). Returns ``False`` for any connection
    error, timeout, or other HTTP error codes.

    Parameters
    ----------
    base_url : str
        Base URL of the server, e.g., ``"http://127.0.0.1:5000"``.
    auth_token : str, optional
        Bearer token for authentication. If provided, it is hashed and sent in the
        Authorization header.
    timeout : float
        Socket timeout in seconds for the probe request.
    ssl_context : ssl.SSLContext, optional
        SSL context for HTTPS connections. Defaults to ``None`` (HTTP only).

    Returns
    -------
    bool
        ``True`` if the server is reachable and responsive, ``False`` otherwise.
    """
    probe_url = f"{base_url}/api/connection/run_mode"
    try:
        req = urllib.request.Request(probe_url, method="GET")
        if auth_token:
            # Build auth header same way as FluentRestClient._make_auth_headers
            auth_hash = hashlib.sha256(auth_token.encode()).hexdigest()
            req.add_header("Authorization", f"Bearer {auth_hash}")
        with urllib.request.urlopen(
            req, timeout=timeout, context=ssl_context
        ):  # nosec B310
            logger.debug("Server reachability probe succeeded: %s", probe_url)
            return True
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            # Auth required — server is up and expecting credentials.
            logger.debug(
                "Server responded with 401 (Unauthorized) — server is reachable: %s",
                probe_url,
            )
            return True
        logger.debug(
            "Server reachability probe failed with HTTP %d: %s", exc.code, probe_url
        )
        return False
    except (urllib.error.URLError, OSError) as exc:
        logger.debug("Server reachability probe failed: %s — %s", probe_url, exc)
        return False


# ---------------------------------------------------------------------------
# Public API — session classes
# ---------------------------------------------------------------------------


class RestSolverSession:
    """Session wrapper for connecting to a running Fluent REST (SimBA) server.

    This class provides a session abstraction over :class:`FluentRestClient`,
    storing connection metadata (IP, port, auth token) and providing effective
    access to the low-level REST client for path-based operations.

    Parameters
    ----------
    base_url : str
        Root URL of the Fluent REST server, e.g., ``"http://127.0.0.1:5000"``.
    auth_token : str, optional
        Raw bearer token (the password set when Fluent was started).
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"`` (solver).
    timeout : float, optional
        HTTP socket timeout in seconds.  Defaults to ``30.0``.
    max_retries : int, optional
        Maximum automatic retries on transient HTTP errors.  Defaults to ``0``.
    retry_delay : float, optional
        Base delay in seconds between retries (exponential back-off).
        Defaults to ``1.0``.
    ssl_context : ssl.SSLContext, optional
        Custom SSL context for HTTPS connections.  Defaults to ``None``.

    Attributes
    ----------
    ip : str
        IP address of the connected server.
    port : int
        TCP port of the connected server.
    auth_token : str
        Bearer token used for authentication.

    Examples
    --------
    >>> from ansys.fluent.core.rest import connect_to_webserver
    >>> session = connect_to_webserver(
    ...     ip="127.0.0.1",
    ...     port=5000,
    ...     auth_token="my-secret-token",
    ... )
    >>> # Access low-level REST client for path-based operations
    >>> client = session._client
    >>> result = client.get_var("setup/models/energy/enabled")
    """

    def __init__(
        self,
        ip: str,
        port: int,
        auth_token: str,
        *,
        scheme: str = "http",
        component: str = "fluent_1",
        timeout: float = 30.0,
        max_retries: int = 0,
        retry_delay: float = 1.0,
        ssl_context: ssl.SSLContext | None = None,
    ) -> None:
        """Initialize a RestSolverSession.

        This is normally called by :func:`connect_to_webserver`, not directly.
        """
        # Store connection parameters (Option B: session owns state)
        self.ip = ip
        self.port = port
        self.auth_token = auth_token
        self._retry_delay = retry_delay
        self._ssl_context = ssl_context

        # Build base_url from components
        base_url = f"{scheme}://{ip}:{port}"

        # Create the low-level REST client
        self._client = FluentRestClient(
            base_url,
            auth_token=auth_token,
            component=component,
            timeout=timeout,
            max_retries=max_retries,
        )

    @property
    def client(self) -> FluentRestClient:
        """The low-level REST client for path-based operations."""
        return self._client

    def exit(self) -> None:
        """Shut down the Fluent server and close the underlying client."""
        self._client.exit()

    def __enter__(self) -> "RestSolverSession":
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager — calls :meth:`exit`."""
        self.exit()


# ---------------------------------------------------------------------------
# Public API — connectors
# ---------------------------------------------------------------------------


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
    ssl_context: ssl.SSLContext | None = None,
) -> RestSolverSession:
    """Connect to an already-running Fluent REST server.

    Use this function when the server is already running and you know
    its ``ip``, ``port``, and ``auth_token``.  For a fully automated local
    launch use :func:`launch_webserver` instead (phase 2).

    Parameters
    ----------
    ip : str
        IP address or hostname of the Fluent server, e.g. ``"127.0.0.1"``.
    port : int
        TCP port the Fluent server is listening on.
    auth_token : str
        Bearer token (password) for authentication.
    scheme : str, optional
        URL scheme.  Must be ``"http"`` or ``"https"``.  Defaults to
        ``"http"``.
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"`` (solver).
    version : str, optional
        Fluent version string (e.g. ``"261"``). Used for logging and metadata.
        Defaults to ``""``.
    timeout : float, optional
        HTTP socket timeout in seconds.  Defaults to ``30.0``.
    max_retries : int, optional
        Maximum automatic retries on transient HTTP errors.  Defaults to
        ``0``.
    retry_delay : float, optional
        Base delay in seconds between retries (exponential back-off).
        Defaults to ``1.0``.
    ssl_context : ssl.SSLContext, optional
        Custom SSL context for HTTPS connections.  If not provided and
        *scheme* is ``"https"``, attempts to auto-discover certificates.
        Defaults to ``None``.

    Returns
    -------
    RestSolverSession
        A fully initialized solver session with ``ip``, ``port``, and
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
    >>> # Access settings via the low-level REST client
    >>> client = session._client
    >>> enabled = client.get_var("setup/models/energy/enabled")
    """
    if scheme not in ("http", "https"):
        raise ValueError(f"scheme must be 'http' or 'https', got {scheme!r}")

    # Determine actual scheme and SSL context
    actual_scheme = scheme
    actual_ssl_context = ssl_context
    probe_timeout = min(timeout, 5.0)

    # If HTTPS requested, try to discover and use certificates
    if scheme == "https":
        if ssl_context is None:
            # Auto-discover certificates
            actual_ssl_context = _get_ssl_context_for_https()
            if actual_ssl_context is None:
                logger.warning(
                    "HTTPS requested but no certificates found. "
                    "Set FLUENT_WEBSERVER_CERTIFICATE_ROOT environment variable "
                    "or check default installation path. Falling back to HTTP."
                )
                actual_scheme = "http"
                actual_ssl_context = None

    base_url = f"{actual_scheme}://{ip}:{port}"

    # Reachability probe — fail-fast before building the session
    probe_result = _probe_server(
        base_url, auth_token, probe_timeout, actual_ssl_context
    )

    # If HTTPS was requested but failed, try HTTP as fallback
    if not probe_result and scheme == "https" and actual_scheme == "https":
        logger.warning(
            "HTTPS probe failed at %s://%s:%d. Attempting HTTP fallback.",
            scheme,
            ip,
            port,
        )
        fallback_base_url = f"http://{ip}:{port}"
        probe_result = _probe_server(fallback_base_url, auth_token, probe_timeout)
        if probe_result:
            actual_scheme = "http"
            base_url = fallback_base_url
            actual_ssl_context = None
            logger.warning(
                "HTTP fallback succeeded. Ensure SSL certificates "
                "are properly installed at FLUENT_WEBSERVER_CERTIFICATE_ROOT."
            )

    # Single error path for all probe failures
    if not probe_result:
        raise ConnectionError(
            f"Fluent server at {base_url} did not respond. "
            f"Verify that the server is running on the given ip and port, "
            f"and that the auth_token is correct."
        )

    # Probe passed — create the session
    session = RestSolverSession(
        ip,
        port,
        auth_token,
        scheme=actual_scheme,
        component=component,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        ssl_context=actual_ssl_context,
    )

    # Log connection (version at DEBUG, connection at INFO)
    logger.info(
        "Connected to Fluent REST server at %s://%s:%d (component=%s)",
        actual_scheme,
        ip,
        port,
        component,
    )

    # Warn if scheme was downgraded from HTTPS to HTTP
    if actual_scheme != scheme:
        logger.warning(
            "Connected via %s instead of requested %s. "
            "For production, ensure SSL certificates are installed.",
            actual_scheme.upper(),
            scheme.upper(),
        )

    if version:
        logger.debug("Fluent version: %s", version)

    return session
