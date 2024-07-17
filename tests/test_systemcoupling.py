import pytest


@pytest.mark.fluent_version(">=24.1")
def test_systemcoupling_mixing_elbow_settings(mixing_elbow_case_data_session):
    """Very superficial test of System Coupling related settings."""
    solver = mixing_elbow_case_data_session
    # check participant type, analysis type, regions, and variables
    assert solver.system_coupling.participant_type == "FLUENT"
    assert solver.system_coupling.get_analysis_type() == "Steady"
    regions = solver.system_coupling.get_regions()
    variables = solver.system_coupling.get_variables()
    # [wall-inlet, wall-elbow, elbow-fluid, hot-inlet, cold-inlet, outlet]
    assert len(regions) >= 6
    # [force, dsip, temp, htc, hflow, nwt, hrate, cond, lorentz-force]
    assert len(variables) >= 9
