import time

import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core import PyFluentInterrupted


@pytest.mark.fluent_version(">=23.1")
def test_fluent_error_interrupt(new_solver_session):
    session = new_solver_session
    with pytest.raises(BaseException) as exc:
        session.scheme_eval.scheme_eval(
            "(events/transmit 'error-event "
            '(cons (format #f "fatal error: ~a~%" "testing") 1))'
        )
        for _ in range(100):
            # exception should usually be raised on or before the first time.sleep() call
            time.sleep(0.1)
    assert exc.type == PyFluentInterrupted
