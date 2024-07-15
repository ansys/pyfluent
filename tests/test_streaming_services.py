import time

from ansys.fluent.core import connect_to_fluent
from ansys.fluent.core.utils.fluent_version import FluentVersion


def transcript(data):
    transcript.data = data


def run_transcript(i, ip, port, password):
    transcript("")
    session = connect_to_fluent(
        ip=ip, port=port, password=password, cleanup_on_exit=False
    )
    session.transcript.register_callback(transcript)

    transcript_checked = False
    transcript_passed = False

    if i % 5 == 0:
        time.sleep(0.5)
        session.scheme_eval.scheme_eval("(pp 'test)")
        time.sleep(0.5)
        if not transcript.data:
            assert transcript.data == ""
        else:
            assert transcript.data == "test"
            transcript_passed = True
        transcript_checked = True

    return transcript_checked, transcript_passed


def test_transcript(new_solver_session):
    solver = new_solver_session
    ip = solver.connection_properties.ip
    port = solver.connection_properties.port
    password = solver.connection_properties.password

    total_checked_transcripts = 0
    total_passed_transcripts = 0

    for i in range(100):
        transcript_checked, transcript_passed = run_transcript(i, ip, port, password)
        total_checked_transcripts += int(transcript_checked)
        total_passed_transcripts += int(transcript_passed)

    if solver.get_fluent_version() >= FluentVersion.v232:
        assert total_checked_transcripts == total_passed_transcripts
    else:
        assert total_checked_transcripts >= total_passed_transcripts
