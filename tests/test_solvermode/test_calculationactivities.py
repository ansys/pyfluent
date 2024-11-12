import pytest

from ansys.fluent.core.utils.fluent_version import FluentVersion


@pytest.mark.fluent_version("latest")
def test_solver_calculation(static_mixer_case_session):
    solver_session = static_mixer_case_session
    scheme_eval = solver_session.scheme_eval.scheme_eval
    assert scheme_eval("(client-get-var 'residuals/plot?)") is True
    # TODO: Remove the if condition after a stable version of 23.1 is available and update the commands as required.
    if solver_session.get_fluent_version() < FluentVersion.v231:
        solver_session.tui.solve.monitors.residual.plot("no")
        assert scheme_eval("(client-get-var 'residuals/plot?)") is False
    assert scheme_eval("(data-valid?)") is False
    solver_session.solution.initialization.hybrid_initialize()
    assert scheme_eval("(data-valid?)") is True
    # solver_session.solution.run_calculation.iterate.get_attr("arguments")
    # solver_session.solution.run_calculation.number_of_iterations = 5
    # assert solver_session.solution.run_calculation.number_of_iterations == 5
