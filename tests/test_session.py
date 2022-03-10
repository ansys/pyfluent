from concurrent import futures

import grpc

from ansys.api.fluent.v0 import health_pb2, health_pb2_grpc
from ansys.fluent.core.services.health_check import HealthCheckService
from ansys.fluent.core.session import Session


class MockHealthServicer(health_pb2_grpc.HealthServicer):
    def Check(self, request, context):  # noqa N802
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.ServingStatus.SERVING
        )


def test_session():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    server.start()
    session = Session(ip=ip, port=port, cleanup_on_exit=False)
    assert session.check_health() == HealthCheckService.Status.SERVING.name
    server.stop(None)
    session.exit()
    assert session.check_health() == HealthCheckService.Status.NOT_SERVING.name
