from concurrent import futures
import os
from pathlib import Path
import tempfile
import time

import grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc
import pytest
from util.meshing_workflow import new_mesh_session  # noqa: F401
from util.solver_workflow import make_new_session, new_solver_session  # noqa: F401

from ansys.api.fluent.v0 import (
    scheme_eval_pb2,
    scheme_eval_pb2_grpc,
    settings_pb2,
    settings_pb2_grpc,
)
from ansys.api.fluent.v0.scheme_pointer_pb2 import SchemePointer
import ansys.fluent.core as pyfluent
from ansys.fluent.core import connect_to_fluent, examples, session
from ansys.fluent.core.fluent_connection import FluentConnection, PortNotProvided
from ansys.fluent.core.launcher.error_handler import LaunchFluentError
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.utils.execution import timeout_loop
from ansys.fluent.core.utils.networking import get_free_port


class MockSettingsServicer(settings_pb2_grpc.SettingsServicer):
    def GetStaticInfo(
        self, request: settings_pb2.GetStaticInfoRequest, context: grpc.ServicerContext
    ) -> settings_pb2.GetStaticInfoResponse:
        response = settings_pb2.GetStaticInfoResponse()
        response.info.type = "Dummy"
        return response

    def GetVar(
        self,
        request: settings_pb2.GetVarRequest,
        context: grpc.ServicerContext,
    ) -> settings_pb2.GetVarResponse:
        response = settings_pb2.GetVarResponse()
        response.value.value_map.SetInParent()
        return response


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


def test_create_mock_session_by_passing_ip_port_password() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = get_free_port()
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    server.start()

    with pytest.raises(PortNotProvided) as msg:
        session = BaseSession(
            FluentConnection(ip=ip, password="12345", cleanup_on_exit=False)
        )

    session = BaseSession(
        FluentConnection(ip=ip, port=port, password="12345", cleanup_on_exit=False)
    )
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


def test_create_mock_session_by_setting_ip_port_env_var(
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


def test_create_mock_session_by_passing_grpc_channel() -> None:
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


def test_create_mock_session_from_server_info_file(tmp_path: Path) -> None:
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
    session = BaseSession._create_from_server_info_file(
        server_info_file_name=str(server_info_file), cleanup_on_exit=False
    )
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


def test_create_mock_session_from_server_info_file_with_wrong_password(
    tmp_path: Path,
) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = get_free_port()
    server.add_insecure_port(f"{ip}:{port}")
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    server.start()
    server_info_file = tmp_path / "server_info.txt"
    server_info_file.write_text(f"{ip}:{port}\n1234")
    with pytest.raises(RuntimeError) as ex:
        session = BaseSession._create_from_server_info_file(
            server_info_file_name=str(server_info_file),
            cleanup_on_exit=False,
        )
        session.scheme_eval.scheme_eval("")
        server.stop(None)
        session.exit()
    assert ex.value.__context__.code() == grpc.StatusCode.UNAUTHENTICATED


def test_create_mock_session_from_launch_fluent_by_passing_ip_port_password() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    ip = "127.0.0.1"
    port = get_free_port()
    server.add_insecure_port(f"{ip}:{port}")
    health_pb2_grpc.add_HealthServicer_to_server(MockHealthServicer(), server)
    scheme_eval_pb2_grpc.add_SchemeEvalServicer_to_server(
        MockSchemeEvalServicer(), server
    )
    settings_pb2_grpc.add_SettingsServicer_to_server(MockSettingsServicer(), server)
    server.start()
    session = connect_to_fluent(
        ip=ip,
        port=port,
        cleanup_on_exit=False,
        password="12345",
    )
    # check a few dir elements
    fields_dir = dir(session.fields)
    for attr in ("field_data", "field_info"):
        assert attr in fields_dir
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


def test_create_mock_session_from_launch_fluent_by_setting_ip_port_env_var(
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
    settings_pb2_grpc.add_SettingsServicer_to_server(MockSettingsServicer(), server)
    server.start()
    monkeypatch.setenv("PYFLUENT_FLUENT_IP", ip)
    monkeypatch.setenv("PYFLUENT_FLUENT_PORT", str(port))
    session = connect_to_fluent(
        cleanup_on_exit=False, ip=ip, port=port, password="12345"
    )
    # check a few dir elements
    fields_dir = dir(session.fields)
    for attr in ("field_data", "field_info"):
        assert attr in fields_dir
    assert session.health_check_service.is_serving
    server.stop(None)
    session.exit()
    assert not session.health_check_service.is_serving


@pytest.mark.parametrize("file_format", ["jou", "py"])
@pytest.mark.fluent_version(">=23.2")
def test_journal_creation(file_format, new_mesh_session):
    fd, file_name = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.{file_format}",
        prefix="pyfluent-",
        dir=str(pyfluent.EXAMPLES_PATH),
    )
    os.close(fd)

    file_name = Path(file_name)

    file_name.touch()
    prev_stat = file_name.stat()
    prev_mtime = prev_stat.st_mtime
    prev_size = prev_stat.st_size
    print(f"prev_stat: {prev_stat}")

    session = new_mesh_session
    if session.connection_properties.inside_container:
        session.journal.start(file_name.name)
    else:
        session.journal.start(file_name)
    session = session.switch_to_solver()
    session.journal.stop()
    new_stat = file_name.stat()
    print(f"new_stat: {new_stat}")
    assert new_stat.st_mtime > prev_mtime or new_stat.st_size > prev_size


@pytest.mark.fluent_version(">=23.2")
def test_start_transcript_file_write(new_mesh_session):
    fd, file_name = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.trn",
        prefix="pyfluent-",
        dir=str(pyfluent.EXAMPLES_PATH),
    )
    os.close(fd)

    file_name = Path(file_name)

    file_name.touch()
    prev_stat = file_name.stat()
    prev_mtime = prev_stat.st_mtime
    prev_size = prev_stat.st_size

    session = new_mesh_session
    session.transcript.start(file_name)
    session = session.switch_to_solver()
    session.transcript.stop()

    new_stat = file_name.stat()
    assert new_stat.st_mtime > prev_mtime or new_stat.st_size > prev_size


@pytest.mark.fluent_version(">=23.1")
def test_expected_interfaces_in_solver_session(new_solver_session):
    assert all(
        intf in dir(new_solver_session) for intf in ("preferences", "tui", "workflow")
    )


@pytest.mark.fluent_version(">=24.1")
def test_solverworkflow_not_in_solver_session(new_solver_session):
    assert "solverworkflow" not in dir(new_solver_session)


@pytest.mark.standalone
@pytest.mark.fluent_version(">=23.2")
def test_read_case_using_lightweight_mode():
    import_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    solver = pyfluent.launch_fluent(
        case_file_name=import_file_name, lightweight_mode=True
    )
    solver.setup.models.energy.enabled = False
    old_fluent_connection_id = id(solver._fluent_connection)
    timeout_loop(
        id(solver._fluent_connection) != old_fluent_connection_id,
        timeout=60,
        idle_period=1,
    )
    timeout_loop(
        solver.setup.models.energy.enabled() == False,
        timeout=60,
        idle_period=1,
    )
    solver.exit()


def test_help_does_not_throw(new_solver_session):
    help(new_solver_session.file.read)


def test_build_from_fluent_connection(make_new_session):
    solver1 = make_new_session()
    solver2 = make_new_session()
    assert solver1.health_check_service.is_serving
    assert solver2.health_check_service.is_serving
    health_check_service1 = solver1.health_check_service
    cortex_pid2 = solver2._fluent_connection.connection_properties.cortex_pid
    solver1.build_from_fluent_connection(solver2._fluent_connection)
    assert solver1.health_check_service.is_serving
    assert solver2.health_check_service.is_serving
    assert not health_check_service1.is_serving
    assert solver1._fluent_connection.connection_properties.cortex_pid == cortex_pid2
    assert solver2._fluent_connection.connection_properties.cortex_pid == cortex_pid2


@pytest.mark.standalone
def test_recover_grpc_error_from_launch_error(monkeypatch: pytest.MonkeyPatch):
    orig_parse_server_info_file = session._parse_server_info_file

    def mock_parse_server_info_file(file_name):
        ip, port, password = orig_parse_server_info_file(file_name)
        return ip, port - 1, password  # provide wrong port

    monkeypatch.setattr(session, "_parse_server_info_file", mock_parse_server_info_file)
    with pytest.raises(LaunchFluentError) as ex:
        solver = pyfluent.launch_fluent()
    # grpc.RpcError -> RuntimeError -> LaunchFluentError
    assert ex.value.__context__.__context__.code() == grpc.StatusCode.UNAVAILABLE


def test_recover_grpc_error_from_connection_error():
    with pytest.raises(RuntimeError) as ex:
        pyfluent.connect_to_fluent(ip="127.0.0.1", port=50000, password="abcdefg")
    assert ex.value.__context__.code() == grpc.StatusCode.UNAVAILABLE


def test_solver_methods(new_solver_session):
    solver = new_solver_session

    if int(solver._version) == 222:
        api_keys = {
            "file",
            "setup",
            "solution",
            "results",
            "parametric_studies",
            "current_parametric_study",
        }
        assert api_keys.issubset(set(dir(solver)))
    if int(solver._version) == 232:
        api_keys = {
            "file",
            "mesh",
            "server",
            "setup",
            "solution",
            "results",
            "parametric_studies",
            "current_parametric_study",
            "parallel",
            "report",
        }
        assert api_keys.issubset(set(dir(solver)))
    if int(solver._version) >= 241:
        api_keys = {
            "file",
            "mesh",
            "server",
            "setup",
            "solution",
            "results",
            "parametric_studies",
            "current_parametric_study",
            "parallel",
        }
        assert api_keys.issubset(set(dir(solver)))


@pytest.mark.fluent_version(">=23.2")
def test_get_set_state_on_solver(new_solver_session):
    solver = new_solver_session
    state = solver.get_state()
    assert state
    solver.set_state(state)


def test_solver_structure(new_solver_session):
    solver = new_solver_session
    with pytest.warns(DeprecationWarning):
        solver.field_data
    with pytest.warns(DeprecationWarning):
        solver.svar_data

    assert {
        "field_data",
        "field_info",
        "field_data_streaming",
        "solution_variable_data",
        "solution_variable_info",
        "reduction",
    }.issubset(set(dir(solver.fields)))
