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

Standalone, direct-to-server REST client — no ``flobject`` settings tree,
no gRPC, no protobuf, no code-generated modules.  The Fluent web server
is the single source of truth; every method makes one HTTP call and
returns the server's JSON response directly.

* :class:`RestSolverSession` – lightweight solver session holding a
  :class:`~ansys.fluent.core.rest.client.FluentRestClient` and exposing
  thin pass-through convenience methods.

* :func:`launch_webserver` – **primary entry point**.  Discovers a free
  local port, generates a secure random auth token, spawns the Fluent
  process with ``-ws -ws-port={port}``, waits until the embedded web
  server is reachable, and returns a connected :class:`RestSolverSession`.

* :func:`connect_to_webserver` – connects to an **already-running** web
  server.  Requires ``ip``, ``port``, and ``auth_token``.

Usage — launch (starts Fluent web server locally)
-------------------------------------------------
::

    from ansys.fluent.core.rest import launch_webserver

    session = launch_webserver()
    print(session.get_var("setup/models/energy/enabled"))
    session.exit()     # terminates the Fluent process

Usage — connect (web server already running)
--------------------------------------------
::

    from ansys.fluent.core.rest import connect_to_webserver

    session = connect_to_webserver("127.0.0.1", 5000, auth_token="my-token")
    session.set_var("setup/models/energy/enabled", False)
"""

from __future__ import annotations

import datetime
import hashlib
import logging
import os
import secrets
import shutil
import socket
import ssl
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from ansys.fluent.core.launcher.process_launch_string import get_fluent_exe_path
from ansys.fluent.core.rest.client import FluentRestClient  # noqa: F401
from ansys.fluent.core.rest.client import FluentRestError  # noqa: F401

__all__ = ["RestSolverSession", "connect_to_webserver", "launch_webserver"]

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_LOCALHOST = "127.0.0.1"

# ---------------------------------------------------------------------------
# TLS certificate management (merged from _tls.py — SRP: owns cert lifecycle)
# ---------------------------------------------------------------------------

# Pre-generated 2048-bit DH parameters (not secret — safe to embed).
# Avoids the 5-30 s runtime cost of generating them on every launch.
_DH_PARAMS_PEM = """\
-----BEGIN DH PARAMETERS-----
MIIBCAKCAQEAmKGBEpRnNBAB8pyS2YWtRogTGITvroAso7vL1WWxMGeyHayuJKVC
8HzD1aiPTITaT+99ECUPj7RST6KH+P299qXWDkseInVn92FnAXIOVPn48mgmOl7A
idzQhoJd+HWEkziZWQqZAKRXvTF/boBlusYrkMsqkKEJ5DLvipIoQ+h+H+1Fr0EG
KPnR0KRDUAJRo9t339TdvSCbGudCEAQdAa/EYU6GA4W/Yi5oZQC5Jwcg5Fyqs9Zq
iPZh7mUFzfWNz84LbWOrB16RXHiD7r476/klbVgkVwhiPmh4MHHLtFLVERi+bxGz
Yoebw+OpAHYdDclt8WJhNnnf1Ukwd/IYVwIBAg==
-----END DH PARAMETERS-----
"""


class _TlsCertificateManager:
    """Manages ephemeral TLS certificates for a single Fluent session.

    Encapsulates the full cert lifecycle: generation → usage → cleanup.
    Each instance generates *one* CA + server certificate pair into a
    temporary directory and builds an :class:`ssl.SSLContext` for the
    client.  Call :meth:`cleanup` (or use the instance as a context
    manager) to delete the temporary files.

    This class exists so that cert generation, the SSL context, and the
    temp-directory cleanup are all co-located in a single object rather
    than spread across free functions and external state (SRP).
    """

    def __init__(self) -> None:
        self.cert_dir: str | None = None
        self.ca_cert_path: str | None = None
        self.ssl_context: ssl.SSLContext | None = None

    # -- generation ------------------------------------------------------

    def generate(self) -> None:
        """Create a temp directory with auto-generated TLS certificate files.

        Generates a fresh CA and server certificate pair using the
        ``cryptography`` library.  The following files are written:

        * ``CA.crt``        — self-signed CA certificate (1-day validity)
        * ``webserver.crt`` — server certificate signed by the CA
        * ``webserver.key`` — unencrypted server private key
        * ``dh.pem``        — pre-generated Diffie-Hellman parameters

        After calling this method, :pyattr:`cert_dir`, :pyattr:`ca_cert_path`,
        and :pyattr:`ssl_context` are all populated.
        """
        cert_dir = tempfile.mkdtemp(prefix="pyfluent_tls_")
        logger.debug("TLS cert directory: %s", cert_dir)

        now = datetime.datetime.now(datetime.timezone.utc)
        one_day = datetime.timedelta(days=1)

        # ── CA key + certificate ────────────────────────────────────────
        ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        ca_name = x509.Name(
            [x509.NameAttribute(NameOID.COMMON_NAME, "PyFluent Auto CA")]
        )
        ca_cert = (
            x509.CertificateBuilder()
            .subject_name(ca_name)
            .issuer_name(ca_name)
            .public_key(ca_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now)
            .not_valid_after(now + one_day)
            .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
            .sign(ca_key, hashes.SHA256())
        )

        # ── Server key + certificate ────────────────────────────────────
        server_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        server_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
        server_cert = (
            x509.CertificateBuilder()
            .subject_name(server_name)
            .issuer_name(ca_name)
            .public_key(server_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now)
            .not_valid_after(now + one_day)
            .add_extension(
                x509.SubjectAlternativeName(
                    [
                        x509.DNSName("localhost"),
                        x509.IPAddress(
                            __import__("ipaddress").IPv4Address("127.0.0.1")
                        ),
                    ]
                ),
                critical=False,
            )
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_encipherment=True,
                    content_commitment=False,
                    data_encipherment=True,
                    key_agreement=False,
                    key_cert_sign=False,
                    crl_sign=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
            .sign(ca_key, hashes.SHA256())
        )

        # ── Write files ─────────────────────────────────────────────────
        ca_cert_path = os.path.join(cert_dir, "CA.crt")
        with open(ca_cert_path, "wb") as f:
            f.write(ca_cert.public_bytes(serialization.Encoding.PEM))

        with open(os.path.join(cert_dir, "webserver.crt"), "wb") as f:
            f.write(server_cert.public_bytes(serialization.Encoding.PEM))

        with open(os.path.join(cert_dir, "webserver.key"), "wb") as f:
            f.write(
                server_key.private_bytes(
                    serialization.Encoding.PEM,
                    serialization.PrivateFormat.TraditionalOpenSSL,
                    serialization.NoEncryption(),
                )
            )

        with open(os.path.join(cert_dir, "dh.pem"), "w") as f:
            f.write(_DH_PARAMS_PEM)

        logger.info("Generated ephemeral TLS certificates in %s", cert_dir)

        self.cert_dir = cert_dir
        self.ca_cert_path = ca_cert_path
        self.ssl_context = self.build_ssl_context(ca_cert_path)

    # -- SSL context (also usable standalone for connect_to_webserver) ---

    @staticmethod
    def build_ssl_context(ca_cert: str) -> ssl.SSLContext:
        """Build an :class:`ssl.SSLContext` that trusts a specific CA certificate.

        This is a **static method** so that :func:`connect_to_webserver`
        can build an SSL context from a user-supplied CA path without
        instantiating a full manager.

        Parameters
        ----------
        ca_cert : str
            Absolute path to a PEM-encoded CA certificate file.

        Returns
        -------
        ssl.SSLContext
        """
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.load_verify_locations(ca_cert)
        return ctx

    # -- cleanup ---------------------------------------------------------

    def cleanup(self) -> None:
        """Remove the temporary certificate directory, if one exists."""
        if self.cert_dir is not None:
            shutil.rmtree(self.cert_dir, ignore_errors=True)
            logger.debug("Cleaned up TLS cert directory: %s", self.cert_dir)
            self.cert_dir = None
            self.ca_cert_path = None
            self.ssl_context = None

    def __enter__(self) -> "_TlsCertificateManager":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.cleanup()


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
            sock.bind((_LOCALHOST, 0))
            return sock.getsockname()[1]
    except OSError as exc:
        raise RuntimeError(
            "Could not find a free local TCP port. " f"OS error: {exc}"
        ) from exc


def _generate_auth_token() -> str:
    """Generate a fresh 4-digit random numeric auth token (1000–9999).

    A new token is generated for **every call** so each launched Fluent
    process gets its own independent credential.  The raw 4-digit number is
    never sent over the wire — it is transmitted as
    ``Authorization: Bearer <SHA-256(token)>``.

    Returns
    -------
    str
        A 4-digit decimal string in the range ``"1000"``–``"9999"``.
    """
    # randbelow(9000) → 0–8999; +1000 → 1000–9999 (guaranteed 4 digits).
    token = str(secrets.randbelow(9000) + 1000)
    logger.debug("Generated per-launch auth token.")
    return token


def _probe_server(
    base_url: str,
    auth_token: str,
    component: str = "fluent_1",
    timeout: float = 5.0,
    ssl_context: ssl.SSLContext | None = None,
) -> bool:
    """Return ``True`` if the Fluent web server responds to an authenticated probe.

    Sends ``HEAD /api/{component}/static-info`` with the auth token.
    This matches the first authenticated settings call used by
    :class:`~ansys.fluent.core.rest.rest_launcher.RestSolverSession`.

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
    ssl_context : ssl.SSLContext, optional
        TLS context for HTTPS connections.

    Returns
    -------
    bool
        ``True`` if the server returns any 2xx response.
    """
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

    Two-phase check:

    * **Phase 1** — TCP connect: waits until the port is open (server process
      is listening).  Polls every 2 s.
    * **Phase 2** — Solver-ready probe: ``GET /api/connection/run_mode``.
      Returns as soon as the solver responds (any HTTP reply, including 401).
      A ``400 Fluent not running`` means the web-server is up but the solver
      is still initialising — keep waiting.  Polls every 3 s.

    Both phases share the same *timeout* deadline so the total wait never
    exceeds *timeout* seconds.

    The URL scheme is auto-detected: ``"https"`` when *ssl_context* is
    provided, ``"http"`` otherwise.

    Parameters
    ----------
    port : int
        TCP port to probe.
    timeout : int
        Maximum total seconds to wait.  Defaults to ``120``.
    ssl_context : ssl.SSLContext, optional
        TLS context for HTTPS connections.  When provided the probe
        URL uses ``https://``; otherwise ``http://``.

    Raises
    ------
    TimeoutError
        If the server is not ready within *timeout* seconds.
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
        raise TimeoutError(
            f"Fluent web server on port {port} did not open within {timeout}s."
        )

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

    Holds a :class:`FluentRestClient` and exposes thin pass-through
    convenience methods.  Every method makes **one** HTTP call and returns
    the server's JSON directly — no local settings tree is built.

    Parameters
    ----------
    base_url : str
        Root URL of the Fluent REST server, e.g. ``"http://127.0.0.1:54321"``.
    auth_token : str, optional
        Bearer token for authentication.
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"``.
    timeout : float, optional
        HTTP socket timeout in seconds.  Defaults to ``30.0``.
    max_retries : int, optional
        Maximum automatic retries on transient errors.  Defaults to ``0``.
    retry_delay : float, optional
        Base delay in seconds between retries.  Defaults to ``1.0``.

    Attributes
    ----------
    client : FluentRestClient
        The underlying REST transport.
    ip : str | None
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
    >>> session.get_var("setup/models/energy/enabled")
    True
    >>> session.set_var("setup/models/energy/enabled", False)
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
        # Lifecycle objects — set by launch_webserver, not by end users.
        _ip: str | None = None,
        _port: int | None = None,
        _process: subprocess.Popen | None = None,
        _tls_manager: _TlsCertificateManager | None = None,
    ) -> None:
        self._client = FluentRestClient(
            base_url,
            auth_token=auth_token,
            component=component,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            ssl_context=ssl_context,
        )
        self.ip: str | None = _ip
        self.port: int | None = _port
        self.auth_token: str | None = auth_token
        self._process: subprocess.Popen | None = _process
        self._tls_manager: _TlsCertificateManager | None = _tls_manager

    # ------------------------------------------------------------------
    # Direct-to-server pass-through methods
    # ------------------------------------------------------------------

    @property
    def client(self) -> "FluentRestClient":
        """Return the underlying REST client for low-level access."""
        return self._client

    def get_static_info(self) -> dict:
        """Return the full settings schema.

        Calls ``GET /api/{component}/static-info``.

        Returns
        -------
        dict
            Nested dict describing the settings tree structure.
        """
        return self._client.get_static_info()

    def get_var(self, path: str) -> object:
        """Return the current value of the setting at *path*.

        Calls ``POST /api/{component}/get_var``.

        Parameters
        ----------
        path : str
            Slash-delimited settings path, e.g.
            ``"setup/models/energy/enabled"``.

        Returns
        -------
        object
            The value — bool, int, float, str, list, or dict.
        """
        return self._client.get_var(path)

    def set_var(self, path: str, value: object) -> None:
        """Set the value of the setting at *path*.

        Calls ``PUT /api/{component}/{path}`` with the raw JSON value.

        Parameters
        ----------
        path : str
            Slash-delimited settings path.
        value : object
            New value (bool, int, float, str, list, or dict).
        """
        self._client.set_var(path, value)

    def get_attrs(self, path: str, attrs: list[str], recursive: bool = False) -> dict:
        """Return requested attributes for the setting at *path*.

        Calls ``GET /api/{component}/{path}?attrs=...``.

        Parameters
        ----------
        path : str
            Slash-delimited settings path.
        attrs : list[str]
            Attribute names, e.g. ``["allowed-values"]``.
        recursive : bool, optional
            Include child attributes.  Defaults to ``False``.

        Returns
        -------
        dict
            Server response with an ``"attrs"`` key.
        """
        return self._client.get_attrs(path, attrs, recursive=recursive)

    def execute_command(self, path: str, **kwargs) -> object:
        """Execute a command at *path*.

        The *path* must be the full settings path to the command, e.g.
        ``"solution/initialization/initialize"`` or
        ``"file/read-case"``.  The trailing component is the command
        name; everything before it is the parent path.

        Calls ``POST /api/{component}/{path}`` with *kwargs* as the
        JSON body.  Handles HTTP 409 confirmation prompts per the
        SettingsServiceClientGuide.

        Parameters
        ----------
        path : str
            Full slash-delimited path to the command.
        **kwargs
            Command arguments forwarded as the JSON request body.

        Returns
        -------
        object
            Command result from the server.
        """
        parts = path.rsplit("/", 1)
        if len(parts) == 2:
            parent, command = parts
        else:
            parent, command = "", parts[0]
        return self._client.execute_cmd(parent, command, **kwargs)

    def execute_query(self, path: str, **kwargs) -> object:
        """Execute a query at *path*.

        Same path convention as :meth:`execute_command`.

        Parameters
        ----------
        path : str
            Full slash-delimited path to the query.
        **kwargs
            Query arguments forwarded as the JSON request body.

        Returns
        -------
        object
            Query result from the server.
        """
        parts = path.rsplit("/", 1)
        if len(parts) == 2:
            parent, query = parts
        else:
            parent, query = "", parts[0]
        return self._client.execute_query(parent, query, **kwargs)

    def get_object_names(self, path: str) -> list[str]:
        """Return child named-object names at *path*.

        Parameters
        ----------
        path : str
            Path to a named-object container.

        Returns
        -------
        list[str]
            Child object names.
        """
        return self._client.get_object_names(path)

    def create_object(self, path: str, name: str) -> None:
        """Create a named child object *name* at *path*.

        Calls ``POST /api/{component}/{path}`` with body
        ``{"name": name}``.

        Parameters
        ----------
        path : str
            Path to the named-object container.
        name : str
            Name of the new child object.
        """
        self._client.create(path, name)

    def delete_object(self, path: str, name: str) -> None:
        """Delete the named child object *name* at *path*.

        Calls ``DELETE /api/{component}/{path}/{name}``.

        Parameters
        ----------
        path : str
            Path to the named-object container.
        name : str
            Name of the child object to delete.
        """
        self._client.delete(path, name)

    def rename_object(self, path: str, new: str, old: str) -> None:
        """Rename a child object at *path* from *old* to *new*.

        Parameters
        ----------
        path : str
            Path to the named-object container.
        new : str
            New name.
        old : str
            Current name.
        """
        self._client.rename(path, new, old)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def exit(self) -> None:
        """Terminate the attached Fluent process (if any) and clean up."""
        proc = self._process
        if proc is not None:
            proc.terminate()
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            self._process = None
        # Delegate TLS cleanup to the manager (SRP)
        if self._tls_manager is not None:
            self._tls_manager.cleanup()
            self._tls_manager = None

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
    component: str = "fluent_1",
    timeout: float = 30.0,
    max_retries: int = 0,
    retry_delay: float = 1.0,
) -> RestSolverSession:
    """Launch a local Fluent process with the embedded web server over HTTPS.

    This is the **primary entry point** for using the REST transport layer.

    TLS certificates are **auto-generated** for every launch — no manual
    certificate setup is required.  The generated CA, server cert, server
    key, and DH params are written to a temporary directory, passed to
    Fluent via ``FLUENT_WEBSERVER_CERTIFICATE_ROOT``, and cleaned up
    when :meth:`RestSolverSession.exit` is called.

    The function performs the following steps automatically:

    1. Generates a random 4-digit numeric auth token for this launch.
    2. Generates ephemeral TLS certificates (CA + server cert).
    3. Discovers a free local TCP port.
    4. Resolves the Fluent executable.
    5. Spawns Fluent with ``-ws -ws-port={port}`` and injects the auth
       token and certificate directory into the subprocess environment.
    6. Waits until the HTTPS server is reachable.
    7. Returns a fully connected :class:`RestSolverSession`.

    Parameters
    ----------
    product_version : str, optional
        Fluent version string, e.g. ``"261"`` or ``"26.1.0"``.
    fluent_path : str, optional
        Explicit path to the Fluent executable.
    dimension : str, optional
        Fluent solver dimension argument.  Defaults to ``"3ddp"``.
    start_timeout : int, optional
        Maximum seconds to wait for the web server.  Defaults to ``60``.
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"`` (solver).
    timeout : float, optional
        HTTP socket timeout in seconds.  Defaults to ``30.0``.
    max_retries : int, optional
        Maximum automatic retries on transient HTTP errors.  Defaults to
        ``0``.
    retry_delay : float, optional
        Base delay in seconds between retries.  Defaults to ``1.0``.

    Returns
    -------
    RestSolverSession
        A fully initialised solver session communicating over HTTPS.

    Raises
    ------
    RuntimeError
        If no free TCP port can be found.
    FileNotFoundError
        If the Fluent executable cannot be located.
    TimeoutError
        If the web server does not start within *start_timeout* seconds.
    Exception
        Any exception during server connection is re-raised after cleanup.

    Examples
    --------
    >>> from ansys.fluent.core.rest import launch_webserver
    >>> session = launch_webserver()
    >>> session.get_var("setup/models/energy/enabled")
    True
    >>> session.exit()
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
        raise RuntimeError(
            f"Fluent process exited immediately with return code "
            f"{process.returncode}. Command: {launch_cmd}"
        )

    # 6 — wait for the web server and construct the session
    # Wrap post-Popen work in try/except so a failure (timeout,
    # auth error, etc.) terminates the spawned process before re-raising.
    try:
        _wait_for_server(port, timeout=start_timeout, ssl_context=ssl_ctx)

        scheme = "https" if ssl_ctx else "http"
        base_url = f"{scheme}://{_LOCALHOST}:{port}"
        session = RestSolverSession(
            base_url,
            auth_token=auth_token,
            component=component,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            ssl_context=ssl_ctx,
            _ip=_LOCALHOST,
            _port=port,
            _process=process,
            _tls_manager=tls,
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


def connect_to_webserver(
    ip: str,
    port: int,
    auth_token: str,
    *,
    component: str = "fluent_1",
    timeout: float = 30.0,
    max_retries: int = 0,
    retry_delay: float = 1.0,
    ca_cert: str | None = None,
) -> RestSolverSession:
    """Connect to an already-running Fluent REST server.

    Use this function when the Fluent web server is already running and you
    know its ``ip``, ``port``, and ``auth_token``.  For a fully automated
    local launch use :func:`launch_webserver` instead.

    The URL scheme is **auto-detected** from the *ca_cert* parameter:

    * ``ca_cert`` provided → ``https://``
    * ``ca_cert`` omitted   → ``http://``

    Parameters
    ----------
    ip : str
        IP address or hostname of the Fluent web server, e.g. ``"127.0.0.1"``.
    port : int
        TCP port the Fluent web server is listening on.
    auth_token : str
        Bearer token (password) for authentication.
    component : str, optional
        DataModel component name.  Defaults to ``"fluent_1"`` (solver).
    timeout : float, optional
        HTTP socket timeout in seconds.  Defaults to ``30.0``.
    max_retries : int, optional
        Maximum automatic retries on transient HTTP errors.  Defaults to
        ``0``.
    retry_delay : float, optional
        Base delay in seconds between retries (exponential back-off).
        Defaults to ``1.0``.
    ca_cert : str, optional
        Path to a PEM-encoded CA certificate file for verifying the
        server's TLS certificate.  When provided the connection uses
        HTTPS; otherwise plain HTTP is used.

    Returns
    -------
    RestSolverSession
        A fully initialised solver session with ``ip``, ``port``, and
        ``auth_token`` attributes set.

    Raises
    ------
    ConnectionError
        If the server does not respond to the reachability probe.

    Examples
    --------
    Connect over plain HTTP (no ``ca_cert``):

    >>> session = connect_to_webserver("127.0.0.1", 5000, auth_token="tok")

    Connect over HTTPS (provide CA certificate):

    >>> session = connect_to_webserver(
    ...     "127.0.0.1", 5000, auth_token="tok",
    ...     ca_cert="/path/to/CA.crt",
    ... )
    """
    ssl_ctx = _TlsCertificateManager.build_ssl_context(ca_cert) if ca_cert else None
    scheme = "https" if ca_cert else "http"
    base_url = f"{scheme}://{ip}:{port}"

    # Reachability probe — fail-fast before building the settings tree.
    if not _probe_server(
        base_url,
        auth_token,
        component=component,
        timeout=min(timeout, 5.0),
        ssl_context=ssl_ctx,
    ):
        raise ConnectionError(
            f"Fluent web server at {base_url} did not respond to the reachability "
            f"probe (GET /api/{component}/static-info). "
            "Verify that the server is running on the given ip and port, "
            "and that the auth_token is correct."
        )

    session = RestSolverSession(
        base_url,
        auth_token=auth_token,
        component=component,
        timeout=timeout,
        max_retries=max_retries,
        retry_delay=retry_delay,
        ssl_context=ssl_ctx,
        _ip=ip,
        _port=port,
    )
    return session
