# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
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

"""
Create certificates for gRPC mutual TLS testing, including support for HPC deployments.

This script generates a complete set of certificates including:
- Certificate Authority (CA) key and certificate
- Server key and certificate(s) (signed by CA)
- Client key and certificate (signed by CA)

All certificates are generated with appropriate extensions for their intended use.

Usage:
    python generate_certs.py [options]
    python -m generate_certs [options]

Examples:
    # Simple usage (creates localhost server cert)
    python generate_certs.py

    # Single custom server
    python generate_certs.py --server myserver

    # Custom client name
    python generate_certs.py --server localhost --client "My Client"

    # Custom certificate validity period (1 year)
    python generate_certs.py --server localhost --days 365

    # HPC deployment with multiple servers
    python -m generate_certs --server node01,192.0.2.1 --server node02,192.0.2.2 --server node23,192.0.2.23

    # Mixed server configurations with custom validity
    python generate_certs.py --server main-server --server worker01 --server worker02,10.0.1.2 --days 1825
"""

import argparse
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import sys

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID


def generate_private_key(key_size: int = 4096) -> rsa.RSAPrivateKey:
    """
    Generate an RSA private key.

    Parameters
    ----------
    key_size : int, optional
        Size of the RSA key in bits, by default 4096

    Returns
    -------
    rsa.RSAPrivateKey
        Generated RSA private key
    """
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )


def save_private_key(key: rsa.RSAPrivateKey, filename: str) -> None:
    """
    Save a private key to a PEM file.

    Parameters
    ----------
    key : rsa.RSAPrivateKey
        The private key to save
    filename : str
        Path to the output file
    """
    with open(filename, "wb") as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


def save_certificate(cert: x509.Certificate, filename: str) -> None:
    """
    Save a certificate to a PEM file.

    Parameters
    ----------
    cert : x509.Certificate
        The certificate to save
    filename : str
        Path to the output file
    """
    with open(filename, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


def create_ca_certificate(
    ca_key: rsa.RSAPrivateKey, validity_days: int
) -> x509.Certificate:
    """
    Create a self-signed CA certificate.

    Parameters
    ----------
    ca_key : rsa.RSAPrivateKey
        The private key for the CA certificate
    validity_days : int
        Number of days the certificate should be valid

    Returns
    -------
    x509.Certificate
        Self-signed CA certificate with appropriate extensions for certificate signing
    """
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COMMON_NAME, "Test CA"),
        ]
    )

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=validity_days))
        .add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True,
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                content_commitment=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .sign(ca_key, hashes.SHA256())
    )

    return cert


def create_server_certificate(
    server_key: rsa.RSAPrivateKey,
    ca_cert: x509.Certificate,
    ca_key: rsa.RSAPrivateKey,
    server_common_name: str,
    validity_days: int,
    san_names: list = None,
) -> x509.Certificate:
    """
    Create a server certificate signed by the CA with optional Subject Alternative Names.

    Parameters
    ----------
    server_key : rsa.RSAPrivateKey
        The private key for the server certificate
    ca_cert : x509.Certificate
        The CA certificate to use as issuer
    ca_key : rsa.RSAPrivateKey
        The CA private key to sign the certificate
    server_common_name : str
        The common name for the server certificate (will be used as CN and primary SAN)
    validity_days : int
        Number of days the certificate should be valid
    san_names : list, optional
        Additional Subject Alternative Names to include, by default None

    Returns
    -------
    x509.Certificate
        Server certificate signed by the CA with SERVER_AUTH extended key usage
    """
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COMMON_NAME, server_common_name),
        ]
    )

    # Build SAN list - always include the CN, plus any additional names
    san_list = [x509.DNSName(server_common_name)]
    if san_names:
        for name in san_names:
            # Skip if it's the same as CN to avoid duplicates
            if name != server_common_name:
                san_list.append(x509.DNSName(name))

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(server_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=validity_days))
        .add_extension(
            x509.SubjectAlternativeName(san_list),
            critical=False,
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                key_cert_sign=False,
                crl_sign=False,
                data_encipherment=False,
                key_agreement=False,
                content_commitment=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.ExtendedKeyUsage(
                [
                    ExtendedKeyUsageOID.SERVER_AUTH,
                ]
            ),
            critical=False,
        )
        .sign(ca_key, hashes.SHA256())
    )

    return cert


def create_client_certificate(
    client_key: rsa.RSAPrivateKey,
    ca_cert: x509.Certificate,
    ca_key: rsa.RSAPrivateKey,
    client_common_name: str,
    validity_days: int,
) -> x509.Certificate:
    """
    Create a client certificate signed by the CA.

    Parameters
    ----------
    client_key : rsa.RSAPrivateKey
        The private key for the client certificate
    ca_cert : x509.Certificate
        The CA certificate to use as issuer
    ca_key : rsa.RSAPrivateKey
        The CA private key to sign the certificate
    client_common_name : str
        The common name for the client certificate
    validity_days : int
        Number of days the certificate should be valid

    Returns
    -------
    x509.Certificate
        Client certificate signed by the CA with CLIENT_AUTH extended key usage
    """
    subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COMMON_NAME, client_common_name),
        ]
    )

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(client_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.now(timezone.utc))
        .not_valid_after(datetime.now(timezone.utc) + timedelta(days=validity_days))
        .add_extension(
            x509.SubjectAlternativeName(
                [
                    x509.DNSName(client_common_name),
                ]
            ),
            critical=False,
        )
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                key_encipherment=True,
                key_cert_sign=False,
                crl_sign=False,
                data_encipherment=False,
                key_agreement=False,
                content_commitment=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.ExtendedKeyUsage(
                [
                    ExtendedKeyUsageOID.CLIENT_AUTH,
                ]
            ),
            critical=False,
        )
        .sign(ca_key, hashes.SHA256())
    )

    return cert


def parse_server_spec(server_spec: str) -> tuple[str, list]:
    """
    Parse a server specification string into primary hostname and SAN list.

    Parameters
    ----------
    server_spec : str
        A comma-separated string like "node01,192.0.2.1" or just "node01"

    Returns
    -------
    tuple[str, list]
        Tuple containing (primary_hostname, [additional_san_names])

    Raises
    ------
    ValueError
        If the server specification is empty or invalid
    """
    names = [name.strip() for name in server_spec.split(",") if name.strip()]
    if not names:
        raise ValueError("Server specification cannot be empty")

    primary_hostname = names[0]
    additional_sans = names[1:] if len(names) > 1 else []

    return primary_hostname, additional_sans


def generate_server_certificates(
    ca_cert: x509.Certificate,
    ca_key: rsa.RSAPrivateKey,
    server_specs: list,
    validity_days: int,
) -> list:
    """
    Generate multiple server certificates based on server specifications.

    Parameters
    ----------
    ca_cert : x509.Certificate
        The CA certificate to sign with
    ca_key : rsa.RSAPrivateKey
        The CA private key to sign with
    server_specs : list
        List of server specification strings in format "hostname[,san1,san2,...]"
    validity_days : int
        Number of days the certificates should be valid

    Returns
    -------
    list
        List of generated certificate filenames
    """
    generated_files = []

    for spec in server_specs:
        primary_hostname, additional_sans = parse_server_spec(spec)

        # If only one server is specified, use 'server' as generic name
        if len(server_specs) == 1:
            filename = "server"
        else:
            filename = primary_hostname

        print(f"Generating server certificate for {primary_hostname}")
        if additional_sans:
            print(f"  Additional SAN names: {', '.join(additional_sans)}")

        # Generate server key and certificate
        server_key = generate_private_key()
        server_cert = create_server_certificate(
            server_key,
            ca_cert,
            ca_key,
            primary_hostname,
            validity_days,
            additional_sans,
        )

        # Save with primary hostname as filename
        key_filename = f"{filename}.key"
        cert_filename = f"{filename}.crt"

        save_private_key(server_key, key_filename)
        save_certificate(server_cert, cert_filename)

        generated_files.extend([key_filename, cert_filename])

    return generated_files


def main():
    """
    Generate all certificates based on command-line arguments.

    This function serves as the main entry point for the certificate generation tool.
    It parses command-line arguments and generates a complete PKI setup including
    CA, server, and client certificates suitable for gRPC mutual TLS.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate certificates for gRPC mutual TLS testing",
        epilog="""
Examples:
  %(prog)s --server localhost
  %(prog)s --server node01,192.0.2.1 --server node02,192.0.2.2 --server node23,192.0.2.23
  %(prog)s --server main-server --server worker01 --server worker02,10.0.1.2
  %(prog)s --server myserver --client "My Client"
  %(prog)s --server localhost --days 365
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--server",
        action="append",
        dest="servers",
        help="Server specification: hostname[,san1,san2,...] (can be used multiple times) (default: localhost)",
    )
    parser.add_argument(
        "--client",
        default="Test Client",
        help="Common name for the client certificate (default: Test Client)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=3650,
        help="Number of days the certificates should be valid (default: 3650, which is 10 years)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("certs"),
        help="Output directory for certificates (default: certs)",
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.servers:
        # Default behavior: create localhost server cert
        args.servers = ["localhost,127.0.0.1"]

    # Create output directory if it doesn't exist
    output_dir = args.output_dir
    output_dir.mkdir(exist_ok=True)

    # Change to output directory
    original_dir = os.getcwd()
    os.chdir(output_dir)

    try:
        generated_files = []

        print("Generating CA key and certificate for self-signing...")
        # Generate CA key and certificate for self-signing
        ca_key = generate_private_key()
        ca_cert = create_ca_certificate(ca_key, args.days)

        save_private_key(ca_key, "ca.key")
        save_certificate(ca_cert, "ca.crt")
        generated_files.extend(["ca.key", "ca.crt"])

        # Generate server certificates
        print(f"Generating {len(args.servers)} server certificate(s)...")
        server_files = generate_server_certificates(
            ca_cert, ca_key, args.servers, args.days
        )
        generated_files.extend(server_files)

        print(f"Generating client certificate (CN: {args.client})...")
        # Generate client key and certificate
        client_key = generate_private_key()
        client_cert = create_client_certificate(
            client_key, ca_cert, ca_key, args.client, args.days
        )

        save_private_key(client_key, "client.key")
        save_certificate(client_cert, "client.crt")
        generated_files.extend(["client.key", "client.crt"])

        print(f"\nDone! Generated {len(generated_files)} files in {output_dir}:")
        for filename in sorted(generated_files):
            print(f"  {filename}")

    except Exception as e:
        print(f"Error generating certificates: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Return to original directory
        os.chdir(original_dir)


if __name__ == "__main__":
    main()
