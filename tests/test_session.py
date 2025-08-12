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

from concurrent import futures
import os
from pathlib import Path
import tempfile
import time

import grpc
from grpc_health.v1 import health_pb2, health_pb2_grpc
import pytest

from ansys.api.fluent.v0 import (
    scheme_eval_pb2,
    scheme_eval_pb2_grpc,
    settings_pb2,
    settings_pb2_grpc,
)
from ansys.api.fluent.v0.scheme_pointer_pb2 import SchemePointer
import ansys.fluent.core as pyfluent
from ansys.fluent.core import connect_to_fluent, examples, session
from ansys.fluent.core.exceptions import BetaFeaturesNotEnabled
from ansys.fluent.core.fluent_connection import FluentConnection, PortNotProvided
from ansys.fluent.core.launcher.error_handler import LaunchFluentError
from ansys.fluent.core.pyfluent_warnings import PyFluentDeprecationWarning
from ansys.fluent.core.session import BaseSession
from ansys.fluent.core.solver.flobject import InactiveObjectError
from ansys.fluent.core.utils.execution import timeout_loop
from ansys.fluent.core.utils.file_transfer_service import ContainerFileTransferStrategy
from ansys.fluent.core.utils.fluent_version import FluentVersion
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


def test_download_file():
    with pytest.raises(examples.RemoteFileNotFoundError):
        examples.download_file(
            "mixing_elbow.cas.h5", "pyfluent/examples/DOE-ML-Mixing-Elbow"
        )


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

    with pytest.raises(PortNotProvided):
        fluent_connection = FluentConnection(
            ip=ip, password="12345", cleanup_on_exit=False
        )
        session = BaseSession(
            fluent_connection=fluent_connection,
            scheme_eval=fluent_connection._connection_interface.scheme_eval,
        )

    fluent_connection = FluentConnection(
        ip=ip, port=port, password="12345", cleanup_on_exit=False
    )
    session = BaseSession(
        fluent_connection=fluent_connection,
        scheme_eval=fluent_connection._connection_interface.scheme_eval,
    )
    assert session.is_server_healthy()
    server.stop(None)
    session.exit()
    assert not session.is_server_healthy()


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
    monkeypatch.setattr(pyfluent.config, "launch_fluent_ip", ip)
    monkeypatch.setattr(pyfluent.config, "launch_fluent_port", port)
    fluent_connection = FluentConnection(password="12345", cleanup_on_exit=False)
    session = BaseSession(
        fluent_connection=fluent_connection,
        scheme_eval=fluent_connection._connection_interface.scheme_eval,
    )
    assert session.is_server_healthy()
    server.stop(None)
    session.exit()
    assert not session.is_server_healthy()


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
    fluent_connection = FluentConnection(
        channel=channel, cleanup_on_exit=False, password="12345"
    )
    session = BaseSession(
        fluent_connection=fluent_connection,
        scheme_eval=fluent_connection._connection_interface.scheme_eval,
    )
    assert session.is_server_healthy()
    server.stop(None)
    session.exit()
    assert not session.is_server_healthy()


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
    assert session.is_server_healthy()
    server.stop(None)
    session.exit()
    assert not session.is_server_healthy()


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
        session.scheme.eval("")
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
    assert session.is_server_healthy()
    server.stop(None)
    session.exit()
    assert not session.is_server_healthy()


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
    monkeypatch.setattr(pyfluent.config, "launch_fluent_ip", ip)
    monkeypatch.setattr(pyfluent.config, "launch_fluent_port", port)
    session = connect_to_fluent(
        cleanup_on_exit=False, ip=ip, port=port, password="12345"
    )
    # check a few dir elements
    fields_dir = dir(session.fields)
    for attr in ("field_data", "field_info"):
        assert attr in fields_dir
    assert session.is_server_healthy()
    server.stop(None)
    session.exit()
    assert not session.is_server_healthy()


@pytest.mark.parametrize("file_format", ["jou", "py"])
@pytest.mark.fluent_version(">=23.2")
def test_journal_creation(file_format, new_meshing_session_wo_exit):
    fd, file_name = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.{file_format}",
        prefix="pyfluent-",
        dir=str(pyfluent.config.examples_path),
    )
    os.close(fd)

    file_name = Path(file_name)

    file_name.touch()
    prev_stat = file_name.stat()
    prev_mtime = prev_stat.st_mtime
    prev_size = prev_stat.st_size
    print(f"prev_stat: {prev_stat}")

    session = new_meshing_session_wo_exit
    if session.connection_properties.inside_container:
        session.journal.start(file_name.name)
    else:
        session.journal.start(str(file_name))
    session = session.switch_to_solver()
    session.journal.stop()
    new_stat = file_name.stat()
    print(f"new_stat: {new_stat}")
    assert new_stat.st_mtime > prev_mtime or new_stat.st_size > prev_size
    session.exit()


@pytest.mark.fluent_version(">=23.2")
def test_start_transcript_file_write(new_meshing_session_wo_exit):
    fd, file_name = tempfile.mkstemp(
        suffix=f"-{os.getpid()}.trn",
        prefix="pyfluent-",
        dir=str(pyfluent.config.examples_path),
    )
    os.close(fd)

    file_name = Path(file_name)

    file_name.touch()
    # prev_stat = file_name.stat()
    # prev_mtime = prev_stat.st_mtime
    # prev_size = prev_stat.st_size

    session = new_meshing_session_wo_exit
    session.transcript.start(file_name)
    session = session.switch_to_solver()
    session.transcript.stop()

    # new_stat = file_name.stat()
    # this assertion is invalid.
    # assert new_stat.st_mtime > prev_mtime or new_stat.st_size > prev_size
    session.exit()


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
    if pyfluent.config.use_file_transfer_service:
        file_transfer_service = ContainerFileTransferStrategy()
        container_dict = {"mount_source": file_transfer_service.mount_source}
        solver = pyfluent.launch_fluent(
            case_file_name=import_file_name,
            lightweight_mode=True,
            container_dict=container_dict,
            file_transfer_service=file_transfer_service,
        )
    else:
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
        not solver.setup.models.energy.enabled(),
        timeout=60,
        idle_period=1,
    )
    solver.exit()


@pytest.mark.standalone
@pytest.mark.fluent_version(">=23.2")
def test_read_case_using_lightweight_mode_exiting():
    import_file_name = examples.download_file(
        "mixing_elbow.cas.h5", "pyfluent/mixing_elbow"
    )
    if pyfluent.config.use_file_transfer_service:
        file_transfer_service = ContainerFileTransferStrategy()
        container_dict = {"mount_source": file_transfer_service.mount_source}
        solver = pyfluent.launch_fluent(
            case_file_name=import_file_name,
            lightweight_mode=True,
            container_dict=container_dict,
            file_transfer_service=file_transfer_service,
        )
    else:
        solver = pyfluent.launch_fluent(
            case_file_name=import_file_name, lightweight_mode=True
        )
    solver.exit()
    assert True


def test_help_does_not_throw(new_solver_session):
    help(new_solver_session.file.read)


@pytest.fixture
def new_solver_session2(new_solver_session):
    return new_solver_session


def test_build_from_fluent_connection(new_solver_session, new_solver_session2):
    solver1 = new_solver_session
    solver2 = new_solver_session2
    assert solver1.is_server_healthy()
    assert solver2.is_server_healthy()
    health_check_service1 = solver1._health_check
    cortex_pid2 = solver2._fluent_connection.connection_properties.cortex_pid
    # The below hack is performed to check the base class method
    # (child class has a method with same name)
    solver1.__class__.__bases__[0]._build_from_fluent_connection(
        solver1,
        fluent_connection=solver2._fluent_connection,
        scheme_eval=solver2._fluent_connection._connection_interface.scheme_eval,
    )
    assert solver1.is_server_healthy()
    assert solver2.is_server_healthy()
    timeout_loop(
        not health_check_service1.is_serving,
        timeout=60,
        idle_period=1,
    )
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
        _ = pyfluent.launch_fluent()
    # grpc.RpcError -> RuntimeError -> LaunchFluentError
    assert ex.value.__context__.__context__.code() == grpc.StatusCode.UNAVAILABLE


def test_solver_methods(new_solver_session):
    solver = new_solver_session

    if solver.get_fluent_version() == FluentVersion.v222:
        api_keys = {
            "file",
            "setup",
            "solution",
            "results",
            "parametric_studies",
            "current_parametric_study",
        }
    if solver.get_fluent_version() in (FluentVersion.v232, FluentVersion.v231):
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
    if solver.get_fluent_version() >= FluentVersion.v241:
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
    assert api_keys.issubset(set(dir(solver.settings)))


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
    with pytest.warns(PyFluentDeprecationWarning):
        solver.svar_data

    assert {
        "field_data",
        "field_info",
        "field_data_streaming",
        "solution_variable_data",
        "solution_variable_info",
        "reduction",
    }.issubset(set(dir(solver.fields)))


@pytest.mark.fluent_version(">=24.2")
def test_general_exception_behaviour_in_session(new_solver_session):
    solver = new_solver_session

    # Read case with non-existent path
    with pytest.raises(RuntimeError, match="File .* not found") as exec_info:
        # File not found
        solver.settings.file.read(
            file_type="case", file_name=r"incorrect_path\incorrect_file.cas.h5"
        )
    # Assert that exception is propagated from the Fluent server
    assert isinstance(exec_info.value.__context__, grpc.RpcError)

    # Iterate with no case
    with pytest.raises(
        InactiveObjectError,
        match="solution.run_calculation.iterate' is currently inactive.",
    ) as exec_info:
        # The object is not active
        solver.solution.run_calculation.iterate(iter_count=5)
    # Assert that exception is not propagated from the Fluent server
    assert not isinstance(exec_info.value.__context__, grpc.RpcError)

    # Write case without any case loaded or created
    with pytest.raises(
        InactiveObjectError,
        match="file.write' is currently inactive.",
    ) as exec_info:
        # Uninitialized case
        solver.file.write(file_name="sample.cas.h5", file_type="case")
    # Assert that exception is not propagated from the Fluent server
    assert not isinstance(exec_info.value.__context__, grpc.RpcError)

    graphics = solver.results.graphics

    fluent_version = solver.get_fluent_version()

    if fluent_version >= FluentVersion.v251:
        with pytest.raises(RuntimeError, match="object is not active") as exec_info:
            graphics.mesh["mesh-1"] = {"surfaces_list": "*"}
            graphics.mesh["mesh-1"].display()
        assert isinstance(exec_info.value.__context__, grpc.RpcError)

    case_file = examples.download_file(
        "mixing_elbow.cas.h5",
        "pyfluent/mixing_elbow",
    )
    solver.settings.file.read(file_type="case", file_name=case_file)
    solver.file.write(file_name="sample.cas.h5", file_type="case")

    graphics.mesh["mesh-1"] = {"surfaces_list": "*"}
    graphics.mesh["mesh-1"].display()

    # Post-process without data
    with pytest.raises(RuntimeError) as exec_info:
        # Invalid result.
        graphics.contour["contour-velocity"] = {
            "field": "velocity-magnitude",
            "surfaces_list": ["wall-elbow"],
        }
        graphics.contour["contour-velocity"].display()
    # Assert that exception is propagated from the Fluent server
    assert isinstance(exec_info.value.__context__, grpc.RpcError)

    solver.solution.run_calculation.iterate(iter_count=5)
    graphics.contour["contour-velocity"] = {
        "field": "velocity-magnitude",
        "surfaces_list": ["wall-elbow"],
    }
    graphics.contour["contour-velocity"].display()

    # Following code does not work in GitHub only.

    # mesh_file_2d = examples.download_file(
    #     "sample_2d_mesh.msh.h5",
    #     "pyfluent/surface_mesh",
    #     return_without_path=False,
    # )

    # if fluent_version >= FluentVersion.v252:
    #     # Error in server:
    #     # This appears to be a surface mesh.\nSurface meshes cannot be read under the /file/read-case functionality.
    #     with pytest.raises(
    #         RuntimeError, match="Surface meshes cannot be read"
    #     ) as exec_info:
    #         solver.settings.file.read(file_type="case", file_name=mesh_file_2d)
    #     # Assert that exception is propagated from the Fluent server
    #     assert isinstance(exec_info.value.__context__, grpc.RpcError)


@pytest.mark.fluent_version(">=23.2")
def test_app_utilities_new_and_old(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session

    assert solver._app_utilities.get_app_mode() == pyfluent.FluentMode.SOLVER

    assert not solver._app_utilities.is_beta_enabled()

    assert not solver._app_utilities.is_wildcard("no")

    assert solver._app_utilities.is_wildcard("yes*")

    assert not solver._app_utilities.is_solution_data_available()

    tmp_path = tempfile.mkdtemp(dir=pyfluent.config.examples_path)

    # when running in a container, only the randomly generated folder name will be seen
    # the full paths will be different between host and container
    tmp_folder = Path(tmp_path).parts[-1]

    solver.chdir(tmp_folder)

    cortex_info = solver._app_utilities.get_controller_process_info()
    solver_info = solver._app_utilities.get_solver_process_info()

    assert Path(cortex_info.working_directory).parts[-1] == tmp_folder

    assert Path(solver_info.working_directory).parts[-1] == tmp_folder


@pytest.mark.standalone
def test_new_launch_fluent_api():
    import ansys.fluent.core as pyfluent

    solver = pyfluent.Solver.from_install()
    assert solver._health_check.check_health() == solver._health_check.Status.SERVING
    assert solver.is_server_healthy()

    ip = solver.connection_properties.ip
    password = solver.connection_properties.password
    port = solver.connection_properties.port

    solver_connected = pyfluent.Solver.from_connection(
        ip=ip, password=password, port=port
    )
    assert (
        solver_connected._health_check.check_health()
        == solver._health_check.Status.SERVING
    )
    assert solver.is_server_healthy()

    solver.exit()
    solver_connected.exit()


def test_new_launch_fluent_api_from_container():
    import ansys.fluent.core as pyfluent
    from ansys.fluent.core.utils.networking import get_free_port

    port_1 = get_free_port()
    port_2 = get_free_port()
    container_dict = {"ports": {f"{port_1}": port_1, f"{port_2}": port_2}}
    solver = pyfluent.Solver.from_container(container_dict=container_dict)
    assert solver._health_check.check_health() == solver._health_check.Status.SERVING
    assert solver.is_server_healthy()
    solver.exit()


def test_new_launch_fluent_api_from_connection():
    import ansys.fluent.core as pyfluent

    solver = pyfluent.Solver.from_container()
    assert solver._health_check.check_health() == solver._health_check.Status.SERVING
    assert solver.is_server_healthy()
    ip = solver.connection_properties.ip
    port = solver.connection_properties.port
    password = solver.connection_properties.password
    with pytest.raises(TypeError):
        pyfluent.Meshing.from_connection(ip=ip, port=port, password=password)
    solver.exit()


@pytest.mark.standalone
@pytest.mark.fluent_version(">=25.1")
def test_launch_in_pyconsole_mode():
    with pyfluent.launch_fluent() as session:
        assert session.scheme.eval("(%cx-pyconsole-activated?)") is True
    with pyfluent.launch_fluent(py=True) as session:
        assert session.scheme.eval("(%cx-pyconsole-activated?)") is True
    with pyfluent.launch_fluent(py=False) as session:
        assert session.scheme.eval("(%cx-pyconsole-activated?)") is False


def test_solver_attr_lookup(new_solver_session):
    solver = new_solver_session
    with pytest.warns(PyFluentDeprecationWarning):
        solver.file
    assert solver.settings.file
    with pytest.raises(AttributeError):
        solver.get_completer_info
    assert solver.settings.get_completer_info
    with pytest.raises(AttributeError):
        solver.xyz
    with pytest.raises(AttributeError):
        solver.settings.xyz


@pytest.mark.fluent_version(">=25.2")
def test_beta_meshing_session(new_meshing_session_wo_exit):
    meshing = new_meshing_session_wo_exit
    assert "topology_based" in dir(meshing)
    assert hasattr(meshing, "topology_based")
    with pytest.raises(BetaFeaturesNotEnabled):
        tp = meshing.topology_based()
    meshing.enable_beta_features()
    assert "topology_based" in dir(meshing)
    assert hasattr(meshing, "topology_based")
    tp = meshing.topology_based()
    assert tp

    assert meshing.is_active() is True
    solver = meshing.switch_to_solver()
    assert meshing.is_active() is False
    assert solver.is_active() is True
    solver.exit()


@pytest.mark.fluent_version(">=25.2")
def test_beta_solver_session(new_solver_session_wo_exit):
    solver = new_solver_session_wo_exit
    assert solver.is_active() is True
    assert "switch_to_meshing" in dir(solver)
    assert hasattr(solver, "switch_to_meshing")
    with pytest.raises(BetaFeaturesNotEnabled):
        meshing = solver.switch_to_meshing()
    solver.enable_beta_features()
    assert "switch_to_meshing" in dir(solver)
    assert hasattr(solver, "switch_to_meshing")
    meshing = solver.switch_to_meshing()

    assert solver.is_active() is False
    assert meshing.is_active() is True
    meshing.exit()


@pytest.mark.fluent_version(">=24.2")
def test_error_raised_for_beta_feature_access_for_older_versions(
    new_meshing_session, new_solver_session
):
    meshing = new_meshing_session
    solver = new_solver_session

    if meshing.get_fluent_version() >= FluentVersion.v252:
        meshing.enable_beta_features()
        assert "topology_based" in dir(meshing)
    else:
        with pytest.raises(RuntimeError):
            meshing.enable_beta_features()

    if solver.get_fluent_version() >= FluentVersion.v252:
        solver.enable_beta_features()
        assert "switch_to_meshing" in dir(solver)
    else:
        with pytest.raises(RuntimeError):
            solver.enable_beta_features()


@pytest.mark.fluent_version(">=25.2")
def test_dir_for_session(new_meshing_session_wo_exit):
    meshing = new_meshing_session_wo_exit

    for attr in [
        "watertight",
        "fault_tolerant",
        "two_dimensional_meshing",
        "fields",
        "scheme",
    ]:
        assert getattr(meshing, attr)
        assert attr in dir(meshing)

    for attr in ["field_data", "field_info", "scheme_eval"]:
        # Deprecated methods are accessible but hidden in dir()
        assert getattr(meshing, attr)
        assert attr not in dir(meshing)

    solver = meshing.switch_to_solver()

    assert dir(meshing) == ["is_active"]

    for attr in ["read_case_lightweight", "settings"]:
        assert getattr(solver, attr)
        assert attr in dir(solver)

    for attr in [
        "field_data",
        "field_info",
        "scheme_eval",
        "svar_data",
        "svar_info",
        "reduction",
    ]:
        # Deprecated methods are accessible but hidden in dir()
        assert getattr(solver, attr)
        assert attr not in dir(solver)

    solver.enable_beta_features()
    meshing_new = solver.switch_to_meshing()

    assert dir(solver) == ["is_active"]
    assert len(dir(meshing_new)) > 1
