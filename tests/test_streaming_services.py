import time

from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.launcher.launcher import get_ansys_version
from ansys.fluent.core.session_solver import Solver


def transcript(data):
    transcript.data = data


def run_transcript(i, ip, port, password):
    solver_session = Solver(
        _FluentConnection(ip=ip, port=port, password=password, cleanup_on_exit=False)
    )
    solver_session.transcript.register_callback(transcript)

    transcript_counter = [0, 0]

    if i % 5 == 0:
        solver_session.scheme_eval.scheme_eval("(pp 'test)")
        check_transcript = True
        time.sleep(1)
        transcript_counter[0] += 1
    else:
        check_transcript = False

    if solver_session:
        solver_session.exit()
        if check_transcript:
            if not transcript.data:
                print(i, "transcript failed.", transcript.data)
            else:
                print(i, "transcript passed:", transcript.data)
                transcript_counter[1] += 1
        transcript("")

    return transcript_counter


def test_transcript(new_solver_session):
    solver = new_solver_session
    ip = solver._channel_str.split(":")[0]
    port = int(solver._channel_str.split(":")[1])
    password = solver._metadata[0][-1]

    total_checked_transcript = 0
    passed_transcript = 0

    for i in range(100):
        transcript_counter = run_transcript(i, ip, port, password)
        total_checked_transcript += transcript_counter[0]
        passed_transcript += transcript_counter[1]

    if get_ansys_version() == "23.2.0":
        assert total_checked_transcript == passed_transcript
    else:
        assert total_checked_transcript > passed_transcript
