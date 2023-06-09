import os
import subprocess
import threading
import time

import psutil
from util.solver_workflow import (  # noqa: F401
    new_solver_session,
    new_solver_session_no_transcript,
)

import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples import download_file


def _read_case(session):
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    session.file.read(file_type="case", file_name=case_path)


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


def get_container_ids_set():
    proc = subprocess.Popen(["docker", "ps", "-q"], stdout=subprocess.PIPE)
    output_bytes = proc.stdout.read()
    output_str = output_bytes.decode()
    ids = output_str.strip().split()
    return set(ids)


def test_server_exits_when_session_goes_out_of_scope(with_launching_container) -> None:
    def f(get_pid):
        session = pyfluent.launch_fluent(mode="solver")
        if get_pid:
            f.server_pid = session.scheme_eval.scheme_eval("(%cx-process-id)")

    if os.getenv("PYFLUENT_START_INSTANCE") == "0":
        containers_before = get_container_ids_set()
        f(get_pid=False)
        time.sleep(10)
        containers_after = get_container_ids_set()
        new_containers = containers_after - containers_before
        assert not new_containers
    else:
        f(get_pid=True)
        time.sleep(10)
        assert not psutil.pid_exists(f.server_pid)


def test_server_does_not_exit_when_session_goes_out_of_scope(
    with_launching_container,
) -> None:
    def f():
        session = pyfluent.launch_fluent(mode="solver", cleanup_on_exit=False)
        f.server_pid = session.scheme_eval.scheme_eval("(%cx-process-id)")

    if os.getenv("PYFLUENT_START_INSTANCE") == "0":
        containers_before = get_container_ids_set()
        f()
        time.sleep(10)
        containers_after = get_container_ids_set()
        new_containers = containers_after - containers_before
        assert new_containers
        for container in new_containers:
            subprocess.Popen(["docker", "stop", container])
    else:
        f()
        time.sleep(10)
        assert psutil.pid_exists(f.server_pid)
        psutil.Process(f.server_pid).kill()


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
    assert isinstance(session.connection_properties.inside_container, bool)


def test_fluent_freeze_kill(
    new_solver_session,
) -> None:
    session = new_solver_session
    _read_case(session=session)

    def _freeze_fluent(s):
        return s.tui.mesh.modify_zones.sep_face_zone_face("interior--fluid", "yes")

    tmp_thread = threading.Thread(target=_freeze_fluent, args=(session,), daemon=True)
    tmp_thread.start()
    tmp_thread.join(5)
    if tmp_thread.is_alive():
        session.exit(0)
        tmp_thread.join()
    else:
        raise Exception("Test should have temporarily frozen Fluent, but did not.")

    time.sleep(1)

    assert session.connection_properties.cortex_host not in get_container_ids_set()
