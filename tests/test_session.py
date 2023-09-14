from concurrent import futures
import os
from pathlib import Path
import tempfile
import time

import grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc
import pytest
from util.meshing_workflow import new_mesh_session  # noqa: F401
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.api.fluent.v0 import scheme_eval_pb2, scheme_eval_pb2_grpc
from ansys.api.fluent.v0.scheme_pointer_pb2 import SchemePointer
import ansys.fluent.core as pyfluent
from ansys.fluent.core import connect_to_fluent, examples
from ansys.fluent.core.examples import download_file
from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.utils.networking import get_free_port


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
        return scheme_eval_pb2.SchemeEvalResponse(output=SchemePointer(b=True))


def test_create_session_by_passing_ip_and_port_and_password() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = get_free_port()
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    session = BaseSession(
        FluentConnection(ip=ip, port=port, password="12345", cleanup_on_exit=False)
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
    port = get_free_port()
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    monkeypatch.setenv("PYFLUENT_FLUENT_IP", ip)
    monkeypatch.setenv("PYFLUENT_FLUENT_PORT", str(port))
    session = BaseSession(FluentConnection(password="12345", cleanup_on_exit=False))
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


def test_create_session_by_passing_grpc_channel() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = get_free_port()
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    channel = grpc.insecure_channel(f"{ip}:{port}")
    session = BaseSession(
        FluentConnection(channel=channel, cleanup_on_exit=False, password="12345")
    )
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


def test_create_session_from_server_info_file(tmp_path: Path) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = get_free_port()
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    server_info_file = tmp_path / "server_info.txt"
    server_info_file.write_text(f"{ip}:{port}\n12345")
    session = BaseSession.create_from_server_info_file(
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
    port = get_free_port()
    server.add_insecure_port(f"{ip}:{port}")
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    server_info_file = tmp_path / "server_info.txt"
    server_info_file.write_text(f"{ip}:{port}\n1234")
    with pytest.raises(RuntimeError):
        session = BaseSession.create_from_server_info_file(
            server_info_filepath=str(server_info_file),
            cleanup_on_exit=False,
            start_timeout=2,
        )
        session.scheme_eval.scheme_eval("")
        server.stop(None)
        session.exit()


def test_create_session_from_launch_fluent_by_passing_ip_and_port_and_password() -> (
    None
):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = get_free_port()
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    session = connect_to_fluent(
        ip=ip,
        port=port,
        cleanup_on_exit=False,
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
    port = get_free_port()
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()
    monkeypatch.setenv("PYFLUENT_FLUENT_IP", ip)
    monkeypatch.setenv("PYFLUENT_FLUENT_PORT", str(port))
    session = connect_to_fluent(cleanup_on_exit=False, password="12345")
    # check a few dir elements
    session_dir = dir(session)
    for attr in ("field_data", "field_info"):
        assert attr in session_dir
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


@pytest.mark.parametrize("file_format", ["jou", "py"])
@pytest.mark.fluent_version(">=23.2")
def test_journal_creation(file_format, new_mesh_session):
    fd, file_path = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.{file_format}",
        prefix="pyfluent-",
        dir=str(pyfluent.EXAMPLES_PATH),
    )
    os.close(fd)

    file_path = Path(file_path)

    file_path.touch()
    prev_stat = file_path.stat()
    prev_mtime = prev_stat.st_mtime
    prev_size = prev_stat.st_size
    print(f"prev_stat: {prev_stat}")

    session = new_mesh_session
    if session.connection_properties.inside_container:
        session.journal.start(file_path.name)
    else:
        session.journal.start(file_path)
    session = session.switch_to_solver()
    session.journal.stop()
    new_stat = file_path.stat()
    print(f"new_stat: {new_stat}")
    assert new_stat.st_mtime > prev_mtime or new_stat.st_size > prev_size


@pytest.mark.skip("Failing in GitHub CI")
def test_old_style_session():
    session = pyfluent.launch_fluent()
    case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    session.solver.root.file.read(file_type="case", file_name=case_path)
    session.solver.tui.report.system.sys_stats()
    session.exit()


@pytest.mark.fluent_version(">=23.2")
def test_start_transcript_file_write(new_mesh_session):
    fd, file_path = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.trn",
        prefix="pyfluent-",
        dir=str(pyfluent.EXAMPLES_PATH),
    )
    os.close(fd)

    file_path = Path(file_path)

    file_path.touch()
    prev_stat = file_path.stat()
    prev_mtime = prev_stat.st_mtime
    prev_size = prev_stat.st_size

    session = new_mesh_session
    session.transcript.start(file_path)
    session = session.switch_to_solver()
    session.transcript.stop()

    new_stat = file_path.stat()
    assert new_stat.st_mtime > prev_mtime or new_stat.st_size > prev_size


@pytest.mark.fluent_version(">=23.1")
def test_solverworkflow_in_solver_session(new_solver_session):
    solver = new_solver_session
    solver_dir = dir(solver)
    for attr in ("preferences", "solverworkflow", "tui", "workflow"):
        assert attr in solver_dir


@pytest.mark.fluent_version(">=23.2")
@pytest.mark.skip("Failing in github")
def test_read_case_using_lightweight_mode():
    import_filename = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    solver = pyfluent.launch_fluent(
        case_filepath=import_filename, lightweight_mode=True
    )
    solver.setup.models.energy.enabled = False
    old_fluent_connection_id = id(solver.fluent_connection)
    while id(solver.fluent_connection) == old_fluent_connection_id:
        time.sleep(1)
    time.sleep(5)
    assert solver.setup.models.energy.enabled() == False
    solver.exit()


def test_help_does_not_throw(new_solver_session):
    help(new_solver_session.file.read)
