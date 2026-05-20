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

"""Auto-generation of ephemeral TLS certificates for the REST transport.

This module creates a short-lived CA and server certificate pair so that
:func:`~ansys.fluent.core.rest.rest_launcher.launch_webserver` can start
Fluent in HTTPS mode without any manual certificate setup.

The certificates are written to a temporary directory that Fluent reads via
``FLUENT_WEBSERVER_CERTIFICATE_ROOT``.  The companion ``CA.crt`` is used
by the Python client to trust the self-signed server.

All generated keys and certificates are ephemeral — valid for 1 day only
and deleted when the session exits.
"""

from __future__ import annotations

import datetime
import logging
import os
import ssl
import tempfile

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Pre-generated 2048-bit DH parameters (not secret — safe to embed).
# Avoids the 5-30 s runtime cost of generating them on every launch.
# ---------------------------------------------------------------------------

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


def generate_tls_cert_dir() -> tuple[str, str]:
    """Create a temp directory with auto-generated TLS certificate files.

    Generates a fresh CA and server certificate pair using the
    ``cryptography`` library.  The following files are written:

    * ``CA.crt`` — self-signed CA certificate (1-day validity)
    * ``webserver.crt`` — server certificate signed by the CA
    * ``webserver.key`` — unencrypted server private key
    * ``dh.pem`` — pre-generated Diffie-Hellman parameters

    Returns
    -------
    tuple[str, str]
        ``(cert_dir, ca_cert_path)`` where *cert_dir* is the absolute
        path to the temporary directory (suitable for
        ``FLUENT_WEBSERVER_CERTIFICATE_ROOT``) and *ca_cert_path* is the
        absolute path to ``CA.crt`` (for the client's SSL context).

    Notes
    -----
    The caller is responsible for cleaning up *cert_dir* (e.g. via
    ``shutil.rmtree``) when the session exits.
    """
    cert_dir = tempfile.mkdtemp(prefix="pyfluent_tls_")
    logger.debug("TLS cert directory: %s", cert_dir)

    now = datetime.datetime.now(datetime.timezone.utc)
    one_day = datetime.timedelta(days=1)

    # ── CA key + certificate ────────────────────────────────────────────
    ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "PyFluent Auto CA")])
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

    # ── Server key + certificate ────────────────────────────────────────
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
                    x509.IPAddress(__import__("ipaddress").IPv4Address("127.0.0.1")),
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

    # ── Write files ─────────────────────────────────────────────────────
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
    return cert_dir, ca_cert_path


def build_ssl_context(ca_cert: str) -> ssl.SSLContext:
    """Build an :class:`ssl.SSLContext` that trusts a specific CA certificate.

    Parameters
    ----------
    ca_cert : str
        Absolute path to a PEM-encoded CA certificate file.

    Returns
    -------
    ssl.SSLContext
        A TLS client context configured to verify the server against
        the given CA certificate.
    """
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.load_verify_locations(ca_cert)
    return ctx
