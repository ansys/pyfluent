import time

import pytest


@pytest.mark.fluent_version(">=23.1")
@pytest.mark.parametrize(
    "error_code,raises",
    [
        (0, pytest.wont_raise()),
        (1, pytest.raises(RuntimeError)),
    ],
)
def test_fluent_fatal_error(error_code, raises, new_solver_session):
    scheme_eval = new_solver_session.scheme_eval.scheme_eval
    with raises:
        scheme_eval(
            "(events/transmit 'error-event "
            f'(cons (format #f "fatal error: ~a~%" "testing") {error_code}))'
        )
        for _ in range(10):
            # as these are mostly instant, exception should usually be raised on the second gRPC call
            scheme_eval("(pp 'fatal_error_testing)")
            time.sleep(0.1)


@pytest.mark.fluent_version(">=25.2")
def test_custom_python_error_via_grpc(datamodel_api_version_new, new_solver_session):
    solver = new_solver_session
    # This may need to be updated if the error type changes in the server
    with pytest.raises(RuntimeError, match="prefereces not found!"):
        solver._se_service.get_state("prefereces", "General")
    with pytest.raises(ValueError, match="Datamodel rules for prefereces not found!"):
        solver._se_service.get_specs("prefereces", "General")
