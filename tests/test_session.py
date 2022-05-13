from concurrent import futures
import os
from pathlib import Path

import pytest

from ansys.api.fluent.v0 import health_pb2, health_pb2_grpc
from ansys.fluent.core import launch_fluent
from ansys.fluent.core.services.health_check import HealthCheckService
from ansys.fluent.core.session import Session
import grpc


class MockHealthServicer(health_pb2_grpc.HealthServicer):
    def Check(self, request, context: grpc.ServicerContext):  # noqa N802
        if "PYFLUENT_LAUNCHED_FROM_FLUENT" not in os.environ:
            metadata = dict(context.invocation_metadata())
            password = metadata.get("password", None)
            if password != "12345":
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                return health_pb2.HealthCheckResponse()
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.ServingStatus.SERVING
        )


def test_create_session_by_passing_ip_and_port(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    monkeypatch.setenv("PYFLUENT_LAUNCHED_FROM_FLUENT", "1")
    server.start()
    session = Session(ip=ip, port=port, cleanup_on_exit=False)
    assert session.check_health() == HealthCheckService.Status.SERVING.name
    server.stop(None)
    session.exit()
    assert session.check_health() == HealthCheckService.Status.NOT_SERVING.name


def test_create_session_by_setting_ip_and_port_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    monkeypatch.setenv("PYFLUENT_LAUNCHED_FROM_FLUENT", "1")
    server.start()
    monkeypatch.setenv("PYFLUENT_FLUENT_IP", ip)
    monkeypatch.setenv("PYFLUENT_FLUENT_PORT", str(port))
    session = Session(cleanup_on_exit=False)
    assert session.check_health() == HealthCheckService.Status.SERVING.name
    server.stop(None)
    session.exit()
    assert session.check_health() == HealthCheckService.Status.NOT_SERVING.name


def test_create_session_by_passing_grpc_channel(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    monkeypatch.setenv("PYFLUENT_LAUNCHED_FROM_FLUENT", "1")
    server.start()
    channel = grpc.insecure_channel(f"{ip}:{port}")
    session = Session(channel=channel, cleanup_on_exit=False)
    assert session.check_health() == HealthCheckService.Status.SERVING.name
    server.stop(None)
    session.exit()
    assert session.check_health() == HealthCheckService.Status.NOT_SERVING.name


def test_create_session_from_server_info_file(tmp_path: Path) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    server.start()
    server_info_file = tmp_path / "server_info.txt"
    server_info_file.write_text(f"{ip}:{port}\n12345")
    session = Session.create_from_server_info_file(
        server_info_filepath=server_info_file, cleanup_on_exit=False
    )
    assert session.check_health() == HealthCheckService.Status.SERVING.name
    server.stop(None)
    session.exit()
    assert session.check_health() == HealthCheckService.Status.NOT_SERVING.name


def test_create_session_from_server_info_file_with_wrong_password(
    tmp_path: Path,
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    server.start()
    server_info_file = tmp_path / "server_info.txt"
    server_info_file.write_text(f"{ip}:{port}\n1234")
    session = Session.create_from_server_info_file(
        server_info_filepath=server_info_file, cleanup_on_exit=False
    )
    assert session.check_health() == HealthCheckService.Status.NOT_SERVING.name
    server.stop(None)
    session.exit()
    assert session.check_health() == HealthCheckService.Status.NOT_SERVING.name


def test_create_session_from_launch_fluent_by_passing_ip_and_port(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    monkeypatch.setenv("PYFLUENT_LAUNCHED_FROM_FLUENT", "1")
    server.start()
    session = launch_fluent(
        start_instance=False, ip=ip, port=port, cleanup_on_exit=False
    )
    assert session.check_health() == HealthCheckService.Status.SERVING.name
    server.stop(None)
    session.exit()
    assert session.check_health() == HealthCheckService.Status.NOT_SERVING.name


def test_create_session_from_launch_fluent_by_setting_ip_and_port_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    monkeypatch.setenv("PYFLUENT_LAUNCHED_FROM_FLUENT", "1")
    server.start()
    monkeypatch.setenv("PYFLUENT_FLUENT_IP", ip)
    monkeypatch.setenv("PYFLUENT_FLUENT_PORT", str(port))
    session = launch_fluent(start_instance=False, cleanup_on_exit=False)
    assert session.check_health() == HealthCheckService.Status.SERVING.name
    server.stop(None)
    session.exit()
    assert session.check_health() == HealthCheckService.Status.NOT_SERVING.name
