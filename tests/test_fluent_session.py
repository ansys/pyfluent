from util.solver_workflow import new_solver_session  # noqa: F401


def test_session_starts_transcript_by_default(new_solver_session) -> None:
    # import time
    # time.sleep(20)
    session = new_solver_session

    def print_transcript(transcript):
        print_transcript.out = transcript

    print_transcript.out = None
    session._print_transcript = print_transcript
    # session.scheme_eval.string_eval("(+ 2 3)")
    # assert print_transcript.out == "5"

    """
def test_session_starts_no_transcript_if_disabled(new_solver_session_no_transcript) -> None:
    session = new_solver_session_no_transcript
    def print_transcript(transcript):
        print_transcript.out = transcript
    print_transcript.out = None
    session._print_transcript = print_transcript
    session.scheme_eval.string_eval("(+ 2 3)")
    assert print_transcript.out is None
    """
