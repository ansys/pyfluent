import time

import pytest
from util.solver_workflow import new_solver_session  # noqa: F401


@pytest.mark.fluent_version(">=23.1")
def test_fluent_fatal_error(new_solver_session):
    session = new_solver_session
    with pytest.raises(RuntimeError) as exc:
        session.scheme_eval.scheme_eval(
            "(events/transmit 'error-event "
            '(cons (format #f "fatal error: ~a~%" "testing") 1))'
        )
        for _ in range(10):
            # as these are mostly instant, exception should usually be raised on the second gRPC call
            session.scheme_eval.scheme_eval("(pp 'fatal_error_testing)")
            time.sleep(0.1)

    assert str(exc.value).startswith("Fatal error identified")
