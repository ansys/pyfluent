from util.solver_workflow import (  # noqa: F401
    new_solver_session,
    new_solver_session_no_transcript,
)

from ansys.fluent.core.examples import download_file


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

    session._print_transcript = print_transcript

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
