import os
import subprocess
import threading
import time

from docker.models.containers import Container
import psutil
from util.solver_workflow import (  # noqa: F401
    new_solver_session,
    new_solver_session_no_transcript,
)

import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples import download_file
from ansys.fluent.core.fluent_connection import get_container
from ansys.fluent.core.utils.execution import timeout_loop


def _read_case(session):
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    session.tui.file.read_case(case_path)


def test_session_starts_transcript_by_default(new_solver_session) -> None:
    session = new_solver_session

    def print_transcript(transcript):
        print_transcript.called = True
        if transcript:
            print_transcript.transcript = transcript

    print_transcript.called = False
    print_transcript.transcript = None

    session.transcript.register_callback(print_transcript)

    _read_case(session=session)

    assert print_transcript.called
    assert print_transcript.transcript


def test_session_starts_no_transcript_if_disabled(
    new_solver_session_no_transcript,
) -> None:
    session = new_solver_session_no_transcript

    def print_transcript(transcript):
        print_transcript.called = True

    print_transcript.called = False

    session.transcript.start(write_to_stdout=False)

    _read_case(session=session)

    assert not print_transcript.called


def test_server_exits_when_session_goes_out_of_scope() -> None:
    def f():
        session = pyfluent.launch_fluent()
        _fluent_host_pid = session.connection_properties.fluent_host_pid
        _cortex_host = session.connection_properties.cortex_host
        _inside_container = session.connection_properties.inside_container
        return _fluent_host_pid, _cortex_host, _inside_container

    fluent_host_pid, cortex_host, inside_container = f()

    timeout_loop(
        lambda: (inside_container and not get_container(cortex_host))
        or (not inside_container and not psutil.pid_exists(fluent_host_pid)),
        60,
    )

    if inside_container:
        assert not get_container(cortex_host)
    else:
        assert not psutil.pid_exists(fluent_host_pid)


def test_server_does_not_exit_when_session_goes_out_of_scope() -> None:
    def f():
        session = pyfluent.launch_fluent(cleanup_on_exit=False)
        _fluent_host_pid = session.connection_properties.fluent_host_pid
        _cortex_host = session.connection_properties.cortex_host
        _inside_container = session.connection_properties.inside_container
        _cortex_pwd = session.connection_properties.cortex_pwd
        return _fluent_host_pid, _cortex_host, _inside_container, _cortex_pwd

    fluent_host_pid, cortex_host, inside_container, cortex_pwd = f()
    time.sleep(10)
    if inside_container:
        assert get_container(cortex_host)
        subprocess.Popen(["docker", "stop", cortex_host])  # cortex_host = container_id
    else:
        from pathlib import Path

        assert psutil.pid_exists(fluent_host_pid)
        if os.name == "nt":
            cleanup_file_ext = "bat"
            cmd_list = []
        elif os.name == "posix":
            cleanup_file_ext = "sh"
            cmd_list = ["bash"]
        else:
            raise Exception("Unrecognized operating system.")
        cleanup_filename = (
            f"cleanup-fluent-{cortex_host}-{fluent_host_pid}.{cleanup_file_ext}"
        )
        print(f"cleanup_filename: {cleanup_filename}")
        cmd_list.append(Path(cortex_pwd, cleanup_filename))
        print(f"cmd_list: {cmd_list}")
        subprocess.Popen(
            cmd_list,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def test_does_not_exit_fluent_by_default_when_connected_to_running_fluent(
    monkeypatch,
) -> None:
    session1 = pyfluent.launch_fluent()
    session2 = pyfluent.connect_to_fluent(
        ip=session1.connection_properties.ip,
        port=session1.connection_properties.port,
        password=session1.connection_properties.password,
    )
    assert session2.health_check_service.is_serving
    session2.exit()

    timeout_loop(
        session1.health_check_service.is_serving,
        5.0,
        expected="truthy",
    )

    assert session1.health_check_service.is_serving
    session1.exit()


def test_exit_fluent_when_connected_to_running_fluent(
    monkeypatch,
) -> None:  # import ansys.fluent.core as pyfluent
    session1 = pyfluent.launch_fluent(cleanup_on_exit=False)
    session2 = pyfluent.connect_to_fluent(
        ip=session1.connection_properties.ip,
        port=session1.connection_properties.port,
        password=session1.connection_properties.password,
        cleanup_on_exit=True,
    )
    session2.exit()

    timeout_loop(
        session1.health_check_service.is_serving,
        5.0,
        expected="falsy",
    )

    assert not session1.health_check_service.is_serving


def test_fluent_connection_properties(
    new_solver_session,
) -> None:
    session = new_solver_session
    assert isinstance(session.connection_properties.ip, str)
    assert isinstance(session.connection_properties.port, int)
    assert isinstance(session.connection_properties.password, str)
    assert isinstance(session.connection_properties.cortex_pwd, str)
    assert isinstance(session.connection_properties.cortex_pid, int)
    assert isinstance(session.connection_properties.cortex_host, str)
    assert isinstance(
        session.connection_properties.inside_container, bool
    ) or isinstance(session.connection_properties.inside_container, Container)
    assert isinstance(session.connection_properties.fluent_host_pid, int)


def test_fluent_freeze_kill(
    new_solver_session,
) -> None:
    session = new_solver_session
    _read_case(session=session)

    def _freeze_fluent(s):
        try:
            s.tui.mesh.modify_zones.sep_face_zone_face("interior--fluid", "yes")
        except RuntimeError as expected_tui_error_from_force_exit:
            return expected_tui_error_from_force_exit
        return

    tmp_thread = threading.Thread(target=_freeze_fluent, args=(session,), daemon=True)
    tmp_thread.start()
    tmp_thread.join(5)
    if tmp_thread.is_alive():
        session.exit(timeout=1, timeout_force=True)
        tmp_thread.join()
    else:
        raise Exception("Test should have temporarily frozen Fluent, but did not.")

    alive = timeout_loop(
        get_container,
        5.0,
        args=(session.connection_properties.cortex_host,),
        expected="falsy",
    )

    assert not alive
