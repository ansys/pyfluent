from concurrent import futures
import os
from pathlib import Path
import tempfile
import time

import grpc
import pytest
from util.meshing_workflow import new_mesh_session  # noqa: F401
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.api.fluent.v0 import (
    health_pb2,
    health_pb2_grpc,
    scheme_eval_pb2,
    scheme_eval_pb2_grpc,
)
import ansys.fluent.core as pyfluent
from ansys.fluent.core import launch_fluent
from ansys.fluent.core.examples import download_file
from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.session import _BaseSession


class MockHealthServicer(health_pb2_grpc.HealthServicer):
    def Check(self, request, context: grpc.ServicerContext):  # noqa N802
        metadata = dict(context.invocation_metadata())
        password = metadata.get("password", None)
        if password != "12345":
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return health_pb2.HealthCheckResponse()
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.ServingStatus.SERVING
        )

    def Watch(self, request, context: grpc.ServicerContext):  # noqa N802
        metadata = dict(context.invocation_metadata())
        password = metadata.get("password", None)
        if password != "12345":
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            yield health_pb2.HealthCheckResponse()

        c = 0
        while c < 2:
            time.sleep(1)
            c += 1
            yield health_pb2.HealthCheckResponse(
                status=health_pb2.HealthCheckResponse.ServingStatus.NOT_SERVING
            )

        time.sleep(1)
        yield health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.ServingStatus.SERVING
        )


class MockSchemeEvalServicer(scheme_eval_pb2_grpc.SchemeEvalServicer):
    def StringEval(self, request, context):
        if request.input == "(cx-version)":
            return scheme_eval_pb2.StringEvalResponse(output="(23 1 0)")

    def SchemeEval(
        self,
        request,
        context: grpc.ServicerContext,
    ) -> scheme_eval_pb2.SchemeEvalResponse:
        metadata = dict(context.invocation_metadata())
        password = metadata.get("password", None)
        if password != "12345":
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            return scheme_eval_pb2.SchemeEvalResponse()


def test_create_session_by_passing_ip_and_port_and_password() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    session = _BaseSession(
        _FluentConnection(ip=ip, port=port, password="12345", cleanup_on_exit=False)
    )
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


def test_create_session_by_setting_ip_and_port_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    monkeypatch.setenv("PYFLUENT_FLUENT_IP", ip)
    monkeypatch.setenv("PYFLUENT_FLUENT_PORT", str(port))
    session = _BaseSession(_FluentConnection(password="12345", cleanup_on_exit=False))
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


def test_create_session_by_passing_grpc_channel() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    channel = grpc.insecure_channel(f"{ip}:{port}")
    session = _BaseSession(
        _FluentConnection(channel=channel, cleanup_on_exit=False, password="12345")
    )
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


def test_create_session_from_server_info_file(tmp_path: Path) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    server_info_file = tmp_path / "server_info.txt"
    server_info_file.write_text(f"{ip}:{port}\n12345")
    session = _BaseSession.create_from_server_info_file(
        server_info_filepath=str(server_info_file), cleanup_on_exit=False
    )
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


def test_create_session_from_server_info_file_with_wrong_password(
    tmp_path: Path,
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    server_info_file = tmp_path / "server_info.txt"
    server_info_file.write_text(f"{ip}:{port}\n1234")
    with pytest.raises(RuntimeError):
        session = _BaseSession.create_from_server_info_file(
            server_info_filepath=str(server_info_file), cleanup_on_exit=False
        )
        session.scheme_eval.scheme_eval("")
        server.stop(None)
        session.exit()


def test_create_session_from_launch_fluent_by_passing_ip_and_port_and_password() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    session = launch_fluent(
        start_instance=False,
        ip=ip,
        port=port,
        cleanup_on_exit=False,
        mode="solver",
        password="12345",
    )
    # check a few dir elements
    session_dir = dir(session)
    for attr in ("field_data", "field_info", "setup", "solution"):
        assert attr in session_dir
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


def test_create_session_from_launch_fluent_by_setting_ip_and_port_env_var(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = 50051
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    monkeypatch.setenv("PYFLUENT_FLUENT_IP", ip)
    monkeypatch.setenv("PYFLUENT_FLUENT_PORT", str(port))
    session = launch_fluent(
        start_instance=False, cleanup_on_exit=False, mode="solver", password="12345"
    )
    # check a few dir elements
    session_dir = dir(session)
    for attr in ("field_data", "field_info"):
        assert attr in session_dir
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


@pytest.mark.dev
@pytest.mark.fluent_232
def test_journal_creation(new_mesh_session, tmp_path=pyfluent.EXAMPLES_PATH):
    session = new_mesh_session

    fd, file_path = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.txt",
        prefix="sample_py_journal-",
        dir=str(tmp_path),
    )
    os.close(fd)

    session.journal.start(file_path)

    session = session.switch_to_solver()

    session.journal.stop()

    with open(file_path) as f:
        returned = f.readlines()

    time.sleep(1)

    assert returned


@pytest.mark.skip("Failing in GitHub CI")
def test_old_style_session(with_launching_container):
    session = pyfluent.launch_fluent()
    case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    session.solver.root.file.read(file_type="case", file_name=case_path)
    session.solver.tui.report.system.sys_stats()
    session.exit()


def test_get_fluent_mode(new_mesh_session):
    session = new_mesh_session
    assert session.fluent_connection.get_current_fluent_mode() == "meshing"
    session = session.switch_to_solver()
    assert session.fluent_connection.get_current_fluent_mode() == "solver"


@pytest.mark.dev
@pytest.mark.fluent_232
def test_start_transcript_file_write(new_mesh_session, tmp_path=pyfluent.EXAMPLES_PATH):
    fd, file_path = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.txt",
        prefix="pyfluent-",
        dir=str(tmp_path),
    )
    os.close(fd)

    session = new_mesh_session
    session.transcript.start(file_path)
    session = session.switch_to_solver()
    session.transcript.stop()

    with open(file_path) as f:
        returned = f.readlines()

    session.exit()

    time.sleep(1)

    assert returned


@pytest.mark.fluent_231
def test_solverworkflow_in_solver_session(new_solver_session):
    solver = new_solver_session
    solver_dir = dir(solver)
    for attr in ("preferences", "solverworkflow", "tui", "workflow"):
        assert attr in solver_dir
