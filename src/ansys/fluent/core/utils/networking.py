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

"""Provides a module to get networking functionality."""

from concurrent import futures
import logging
import socket
from typing import Any
import urllib.request

import grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc

network_logger = logging.getLogger("pyfluent.networking")


def get_free_port() -> int:
    """Identifies a free port to which a new socket connection can be established.

    Returns
    -------
    int
        port number
    """
    with socket.socket() as s:
        s.bind(("localhost", 0))
        free_port = s.getsockname()[1]
    return free_port


class _HealthServicer(health_pb2_grpc.HealthServicer):
    def Check(self, request, context: grpc.ServicerContext):
        """Check the status of service."""
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.ServingStatus.SERVING
        )


class _GrpcServer:
    def __init__(self, address: str):
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self._server.add_insecure_port(address)
        health_pb2_grpc.add_HealthServicer_to_server(_HealthServicer(), self._server)
        self._server.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self._server.stop(None)


def find_remoting_ip() -> str:
    """Find an ip address at which a gRPC connection can be established by looping over
    getaddrinfo output.

    Returns
    -------
    str
        remoting ip address
    """
    from ansys.fluent.core import config

    all_ips = [
        addrinfo[-1][0]
        for addrinfo in socket.getaddrinfo(
            "localhost",
            0,
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            flags=socket.AI_PASSIVE,
        )
    ]
    # Check if we can establish a gRPC connection using localhost first
    # before trying other IPs. It has been observed that in some systems,
    # although we can establish a test gRPC connection using one of the
    # resolved IP addresses in addrinfo, PyFluent fails to connect to Fluent
    # using that IP address. Using localhost usually helps in such cases.
    all_ips.insert(0, "localhost")

    for ip in all_ips:
        port = get_free_port()
        address = f"{ip}:{port}"
        with _GrpcServer(address):
            with grpc.insecure_channel(address) as channel:
                stub = health_pb2_grpc.HealthStub(channel)
                try:
                    if (
                        stub.Check(
                            health_pb2.HealthCheckRequest(),
                            timeout=config.infer_remoting_ip_timeout_per_ip,
                        ).status
                        == health_pb2.HealthCheckResponse.ServingStatus.SERVING
                    ):
                        network_logger.debug(f"Can use {ip} as remoting ip")
                        return ip
                except Exception:
                    network_logger.debug(f"Cannot use {ip} as remoting ip")


def check_url_exists(url: str) -> bool:
    """Check if a URL exists.

    Parameters
    ----------
    url : str
        URL to check

    Returns
    -------
    bool
        True if the URL exists, False otherwise
    """
    try:
        with urllib.request.urlopen(url) as response:
            return response.status == 200
    except Exception:
        return False


def get_url_content(url: str) -> str:
    """Get the content of a URL.

    Parameters
    ----------
    url : str
        URL to get content from

    Returns
    -------
    str
        content of the URL
    """
    with urllib.request.urlopen(url) as response:
        return response.read()
