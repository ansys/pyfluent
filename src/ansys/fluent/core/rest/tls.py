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

"""TLS certificate discovery and verification for the Fluent REST transport.

This module does **not** generate certificates — that is the user's
responsibility.  Fluent's embedded web server expects the following files
in a certificate directory:

* ``webserver.crt`` — the SSL certificate file
* ``webserver.key`` — the corresponding private key file
* ``dh.pem``        — the DH parameter file

The certificate directory is resolved in the following order:

1. An explicit ``cert_dir`` parameter passed to :func:`_find_cert_dir`.
2. The ``FLUENT_WEBSERVER_CERTIFICATE_ROOT`` environment variable.
3. The default location inside the Fluent installation:
   ``<AWP_ROOT>/FluidsOne/web/certificate/``

If none of the above provides valid certificate files, the web server
starts in plain HTTP mode.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
import ssl

logger = logging.getLogger(__name__)

# Files that Fluent's embedded web server expects.
_REQUIRED_CERT_FILES = ("webserver.crt", "webserver.key", "dh.pem")


def _find_cert_dir(cert_dir: str | None = None) -> str | None:
    """Discover a certificate directory containing all required files.

    Resolution order:

    1. Explicit *cert_dir* parameter (highest priority).
    2. ``FLUENT_WEBSERVER_CERTIFICATE_ROOT`` environment variable.
    3. Default Fluent install path ``<AWP_ROOT>/FluidsOne/web/certificate/``.

    Parameters
    ----------
    cert_dir : str, optional
        Explicit path to a certificate directory.  When provided and
        valid, it takes precedence over all other sources.

    Returns
    -------
    str or None
        Absolute path to the certificate directory, or ``None`` if no
        valid directory was found.
    """
    # 1. Explicit parameter
    if cert_dir and _verify_cert_dir(cert_dir):
        logger.info("Using certificates from explicit cert_dir: %s", cert_dir)
        return cert_dir

    if cert_dir:
        logger.warning(
            "Explicit cert_dir='%s' but required files missing (%s).",
            cert_dir,
            ", ".join(_REQUIRED_CERT_FILES),
        )

    # 2. Environment variable
    env_dir = os.environ.get("FLUENT_WEBSERVER_CERTIFICATE_ROOT")
    if env_dir and _verify_cert_dir(env_dir):
        logger.info(
            "Using certificates from FLUENT_WEBSERVER_CERTIFICATE_ROOT: %s",
            env_dir,
        )
        return env_dir

    if env_dir:
        logger.warning(
            "FLUENT_WEBSERVER_CERTIFICATE_ROOT='%s' but required files "
            "missing (%s).",
            env_dir,
            ", ".join(_REQUIRED_CERT_FILES),
        )

    # 3. Default Fluent installation path via AWP_ROOTnnn
    default_dir = _get_default_cert_dir()
    if default_dir and _verify_cert_dir(default_dir):
        logger.info("Using certificates from default Fluent path: %s", default_dir)
        return default_dir

    return None


def _get_default_cert_dir() -> str | None:
    """Return the default certificate directory from the Fluent install.

    Scans ``AWP_ROOTnnn`` environment variables (highest version first)
    and returns ``<AWP_ROOT>/FluidsOne/web/certificate/`` if it exists.

    Returns
    -------
    str or None
        Path to the default certificate directory, or ``None``.
    """
    awp_vars = sorted(
        (
            (k, v)
            for k, v in os.environ.items()
            if k.startswith("AWP_ROOT") and k[8:].isdigit()
        ),
        key=lambda kv: int(kv[0][8:]),
        reverse=True,
    )
    for var_name, awp_root in awp_vars:
        cert_path = Path(awp_root) / "FluidsOne" / "web" / "certificate"
        if cert_path.is_dir():
            logger.debug("Found default cert dir via %s: %s", var_name, cert_path)
            return str(cert_path)
    return None


def _verify_cert_dir(cert_dir: str) -> bool:
    """Return ``True`` if *cert_dir* contains all required certificate files.

    Required files: ``webserver.crt``, ``webserver.key``, ``dh.pem``.

    Parameters
    ----------
    cert_dir : str
        Path to the directory to check.

    Returns
    -------
    bool
    """
    d = Path(cert_dir)
    if not d.is_dir():
        return False
    missing = [f for f in _REQUIRED_CERT_FILES if not (d / f).is_file()]
    if missing:
        logger.debug("Cert dir '%s' missing files: %s", cert_dir, missing)
        return False
    return True


def _build_ssl_context(cert_dir: str) -> ssl.SSLContext:
    """Build an SSL context from the certificates in *cert_dir*.

    Loads ``webserver.crt`` as the CA trust anchor so that the client
    trusts the server's self-signed certificate.

    Parameters
    ----------
    cert_dir : str
        Directory containing ``webserver.crt``, ``webserver.key``,
        ``dh.pem``.

    Returns
    -------
    ssl.SSLContext

    Raises
    ------
    FileNotFoundError
        If any required file is missing from *cert_dir*.
    ssl.SSLError
        If the certificate files are invalid or cannot be loaded.
    """
    cert_path = Path(cert_dir)
    for name in _REQUIRED_CERT_FILES:
        f = cert_path / name
        if not f.is_file():
            raise FileNotFoundError(f"Required certificate file not found: {f}")

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.load_verify_locations(str(cert_path / "webserver.crt"))
    logger.debug("SSL context built from certificates in %s", cert_dir)
    return ctx
