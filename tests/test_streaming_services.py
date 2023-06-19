import time

from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core.fluent_connection import FluentConnection
from ansys.fluent.core.session_solver import Solver


def transcript(data):
    transcript.data = data


def run_transcript(i, ip, port, password):
    solver_session = Solver(
        FluentConnection(ip=ip, port=port, password=password, cleanup_on_exit=False)
    )
    solver_session.transcript.register_callback(transcript)

    transcript_checked = transcript_passed = 0

    if i % 5 == 0:
        solver_session.scheme_eval.scheme_eval("(pp 'test)")
        check_transcript = True
        time.sleep(5)
        transcript_checked = 1
    else:
        check_transcript = False

    if solver_session:
        solver_session.exit()
        if check_transcript:
            if not transcript.data:
                assert transcript.data == ""
            else:
                assert transcript.data == "test"
                transcript_passed = 1
        transcript("")

    return transcript_checked, transcript_passed


def test_transcript(new_solver_session):
    solver = new_solver_session
    ip = solver.fluent_connection._channel_str.split(":")[0]
    port = int(solver.fluent_connection._channel_str.split(":")[1])
    password = solver.fluent_connection._metadata[0][-1]

    total_checked_transcript = 0
    passed_transcript = 0

    for i in range(100):
        transcript_checked, transcript_passed = run_transcript(i, ip, port, password)
        total_checked_transcript += transcript_checked
        passed_transcript += transcript_passed

    if solver.get_fluent_version() >= "23.2.0":
        assert total_checked_transcript == passed_transcript
    else:
        assert total_checked_transcript >= passed_transcript
