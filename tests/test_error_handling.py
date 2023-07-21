import time

import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import PyFluentInterrupted


@pytest.mark.fluent_version(">=23.1")  # error-event was added in 23.1
def test_fluent_error_interrupt(new_solver_session):
    session = new_solver_session
    with pytest.raises(BaseException) as exc:
        # (events/transmit 'error-event (cons (format #f "fatal error: ~a~%" "testing") 1))
        session.scheme_eval.scheme_eval(
            "(events/transmit 'error-event "
            '(cons (format #f "fatal error: ~a~%" "testing") 1))'
        )
        for _ in range(100):
            time.sleep(0.1)
        # due to Python limitations, interrupt is scheduled in a queue and not instant
    assert exc.type == PyFluentInterrupted
