import time

import psutil
from util.solver_workflow import (  # noqa: F401
    new_solver_session,
    new_solver_session_no_transcript,
)

import ansys.fluent.core as pyfluent
from ansys.fluent.core.examples import download_file
from ansys.fluent.core.session import Session


def _read_case(session):
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    session.solver.root.file.read(file_type="case", file_name=case_path)


def test_session_starts_transcript_by_default(new_solver_session) -> None:
    session = new_solver_session

    def print_transcript(transcript):
        print_transcript.called = True
        if transcript:
            print_transcript.transcript = transcript

    print_transcript.called = False
    print_transcript.transcript = None

    Session._print_transcript = print_transcript

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

    session._print_transcript = print_transcript

    _read_case(session=session)

    assert not print_transcript.called


def test_server_exits_when_session_goes_out_of_scope() -> None:
    def f():
        session = pyfluent.launch_fluent()
        f.server_pid = session.scheme_eval.scheme_eval("(%cx-process-id)")

    f()
    time.sleep(10)
    assert not psutil.pid_exists(f.server_pid)


def test_server_does_not_exit_when_session_goes_out_of_scope() -> None:
    def f():
        session = pyfluent.launch_fluent(cleanup_on_exit=False)
        f.server_pid = session.scheme_eval.scheme_eval("(%cx-process-id)")

    f()
    time.sleep(10)
    assert psutil.pid_exists(f.server_pid)
    psutil.Process(f.server_pid).kill()
