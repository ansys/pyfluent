from concurrent import futures
import socket
from typing import Any

import grpc

from ansys.api.fluent.v0 import health_pb2, health_pb2_grpc


def get_free_port() -> int:
    """Identifies a free port to which a new socket connection can be
    established.

    Returns
    -------
    int
        port number
    """
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]


class HealthServicer(health_pb2_grpc.HealthServicer):
    def Check(self, request, context: grpc.ServicerContext):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.ServingStatus.SERVING
        )


class GrpcServer:
    def __init__(self, address: str):
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self._server.add_insecure_port(address)
        health_pb2_grpc.add_HealthServicer_to_server(HealthServicer(), self._server)
        self._server.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        self._server.stop(None)


def get_remoting_ip():
    for addrinfo in socket.getaddrinfo(
        socket.gethostname(),
        0,
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        flags=socket.AI_PASSIVE,
    ):
        ip = addrinfo[-1][0]
        port = get_free_port()
        address = f"{ip}:{port}"
        with GrpcServer(address) as server:
            with grpc.insecure_channel(address) as channel:
                stub = health_pb2_grpc.HealthStub(channel)
                try:
                    if (
                        stub.Check(health_pb2.HealthCheckRequest()).status
                        == health_pb2.HealthCheckResponse.ServingStatus.SERVING
                    ):
                        return ip
                except Exception:
                    pass
