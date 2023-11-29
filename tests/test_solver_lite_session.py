import pytest

import ansys.fluent.core as pyfluent


@pytest.mark.fluent_version(">=23.1")
def test_solver_lite_session():
    solver_lite_session = pyfluent.launch_fluent(mode=pyfluent.FluentMode.SOLVER_LITE)
    assert solver_lite_session.__class__.__name__ == "SolverLite"
    assert "switch_to_full_solver" in dir(solver_lite_session)
