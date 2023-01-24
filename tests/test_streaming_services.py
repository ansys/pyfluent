import time

from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core.fluent_connection import _FluentConnection
from ansys.fluent.core.session_solver import Solver


def transcript(data):
    transcript.data = data


def run_transcript(i, ip, port, password):
    solver_session = Solver(_FluentConnection(ip=ip, port=port, password=password, cleanup_on_exit=False))
    solver_session.transcript.register_callback(
        transcript
    )

    if i % 5 == 0:
        solver_session.scheme_eval.scheme_eval("(pp 'test)")
        check_transcript = True
        time.sleep(1)
    else:
        check_transcript = False

    if solver_session:
        solver_session.exit()
        if check_transcript:
            if not transcript.data:
                print(i, 'transcript failed.', transcript.data)
            else:
                print(i, 'transcript passed:', transcript.data)
        transcript("")


def test_transcript(new_solver_session):
    solver = new_solver_session
    ip = solver._channel_str.split(":")[0]
    port = int(solver._channel_str.split(":")[1])
    password = solver._metadata[0][-1]
    for i in range(100):
        run_transcript(i, ip, port, password)
