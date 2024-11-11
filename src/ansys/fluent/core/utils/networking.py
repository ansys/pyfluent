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
    from ansys.fluent.core import INFER_REMOTING_IP_TIMEOUT_PER_IP

    for addrinfo in socket.getaddrinfo(
        "localhost",
        0,
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        flags=socket.AI_PASSIVE,
    ):
        ip = addrinfo[-1][0]
        port = get_free_port()
        address = f"{ip}:{port}"
        with _GrpcServer(address):
            with grpc.insecure_channel(address) as channel:
                stub = health_pb2_grpc.HealthStub(channel)
                try:
                    if (
                        stub.Check(
                            health_pb2.HealthCheckRequest(),
                            timeout=INFER_REMOTING_IP_TIMEOUT_PER_IP,
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
