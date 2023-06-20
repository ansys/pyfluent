import time

import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

import ansys.fluent.core as pyfluent


def transcript(data):
    transcript.data = data


def run_transcript(i, ip, port, password):
    transcript("")
    solver_session = pyfluent.launch_fluent(
        start_instance=False, ip=ip, port=port, password=password, cleanup_on_exit=False
    )
    solver_session.transcript.register_callback(transcript)

    transcript_checked = False
    transcript_passed = False

    if i % 5 == 0:
        solver_session.scheme_eval.scheme_eval("(pp 'test)")
        transcript_checked = True
        time.sleep(5)

    if transcript_checked:
        if not transcript.data:
            assert transcript.data == ""
        else:
            assert transcript.data == "test"
            transcript_passed = True

    return transcript_checked, transcript_passed


def test_transcript(new_solver_session, monkeypatch: pytest.MonkeyPatch):
    solver = new_solver_session
    monkeypatch.setenv("PYFLUENT_LAUNCH_CONTAINER", "0")
    ip = solver.connection_properties.ip
    port = solver.connection_properties.port
    password = solver.connection_properties.password

    total_checked_transcripts = 0
    total_passed_transcripts = 0

    for i in range(100):
        transcript_checked, transcript_passed = run_transcript(i, ip, port, password)
        total_checked_transcripts += int(transcript_checked)
        total_passed_transcripts += int(transcript_passed)

    if solver.get_fluent_version() >= "23.2.0":
        assert total_checked_transcripts == total_passed_transcripts
    else:
        assert total_checked_transcripts >= total_passed_transcripts
