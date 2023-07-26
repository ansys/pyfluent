import pytest


@pytest.mark.nightly
@pytest.mark.quick
@pytest.mark.setup
@pytest.mark.fluent_version(">=23.1")
def test_expression(load_mixing_elbow_mesh):
    solver_session = load_mixing_elbow_mesh
    solver_session.setup.models.energy.enabled = True
    solver_session.setup.named_expressions["r"] = {}
    solver_session.setup.named_expressions["r"] = {
        "definition": "(Position.z**2.0 +Position.x**2.0)**0.5"
    }
    solver_session.setup.named_expressions["r1"] = {}
    solver_session.setup.named_expressions["r1"] = {"definition": "1-(r/0.014[m])"}
    solver_session.setup.named_expressions["v1"] = {}
    solver_session.setup.named_expressions["v1"] = {"definition": "r1**(1.0/6.0)"}
    solver_session.setup.named_expressions["vel_cold"] = {}
    solver_session.setup.named_expressions["vel_cold"] = {
        "definition": "1.264 * 1.43 [m s^-1] * max(0,v1)"
    }
    assert (
        solver_session.setup.named_expressions["r"].definition()
        == "(Position.z**2.0 +Position.x**2.0)**0.5"
    )
    assert solver_session.setup.named_expressions["r1"].definition() == "1-(r/0.014[m])"
    assert solver_session.setup.named_expressions["v1"].definition() == "r1**(1.0/6.0)"
    assert (
        solver_session.setup.named_expressions["vel_cold"].definition()
        == "1.264 * 1.43 [m s^-1] * max(0,v1)"
    )
    solver_session.setup.boundary_conditions.velocity_inlet["cold-inlet"] = {
        "vmag": "vel_cold",
        "turb_intensity": 0.0999999,
        "turb_hydraulic_diam": 1.0,
    }
    solver_session.setup.boundary_conditions.velocity_inlet["hot-inlet"] = {
        "vmag": "max(vel_cold, 1.5 [m/s])"
    }
    assert solver_session.setup.boundary_conditions.velocity_inlet[
        "cold-inlet"
    ].vmag() == {"option": "value", "value": "vel_cold"}
    assert solver_session.setup.boundary_conditions.velocity_inlet[
        "hot-inlet"
    ].vmag() == {"option": "value", "value": "max(vel_cold, 1.5 [m/s])"}
