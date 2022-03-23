import os
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


_IP_ENV_VAR_NAME = "PYFLUENT_FLUENT_IP"
_PORT_ENV_VAR_NAME = "PYFLUENT_FLUENT_PORT"


def test_create_session_by_passing_ip_and_port():
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


def test_create_session_by_setting_ip_and_port_env_var():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    server.start()
    os.environ[_IP_ENV_VAR_NAME] = ip
    os.environ[_PORT_ENV_VAR_NAME] = str(port)
    session = Session(cleanup_on_exit=False)
    assert session.check_health() == HealthCheckService.Status.SERVING.name
    server.stop(None)
    session.exit()
    assert session.check_health() == HealthCheckService.Status.NOT_SERVING.name
    del os.environ[_IP_ENV_VAR_NAME], os.environ[_PORT_ENV_VAR_NAME]

def test_create_session_by_passing_grpc_channel():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    server.start()
    channel = grpc.insecure_channel(f"{ip}:{port}")
    session = Session(channel=channel, cleanup_on_exit=False)
    assert session.check_health() == HealthCheckService.Status.SERVING.name
    server.stop(None)
    session.exit()
    assert session.check_health() == HealthCheckService.Status.NOT_SERVING.name
