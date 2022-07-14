import pytest


@pytest.mark.integration
@pytest.mark.quick
def test_solver_calculation(load_mixing_elbow_mesh):
    session = load_mixing_elbow_mesh
    assert session.scheme_eval.scheme_eval("(client-get-var 'residuals/plot?)") == True
    session.solver.tui.solve.monitors.residual.plot("no")
    assert session.scheme_eval.scheme_eval("(client-get-var 'residuals/plot?)") == False
    assert session.scheme_eval.scheme_eval("(data-valid?)") == False
    session.solver.root.solution.initialization.hybrid_initialize()
    assert session.scheme_eval.scheme_eval("(data-valid?)") == True
    # session.solver.root.solution.run_calculation.iterate.get_attr("arguments")
    # session.solver.root.solution.run_calculation.number_of_iterations = 5
    # assert session.solver.root.solution.run_calculation.number_of_iterations == 5
