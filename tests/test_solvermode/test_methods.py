import pytest


@pytest.mark.settings_only
@pytest.mark.fluent_version("latest")
def test_methods(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session
    solver.setup.models.multiphase.models = "vof"
    solver.setup.general.operating_conditions.gravity = {
        "enable": True,
        "components": [0.0, 0.0, -9.81],
    }
    solver.setup.general.solver.time = "steady"

    p_v_coupling = solver.solution.methods.p_v_coupling
    p_v_coupling.flow_scheme = "Coupled"
    p_v_coupling.coupled_form = False
    assert p_v_coupling() == {
        "flow_scheme": "Coupled",
        "coupled_form": False,
    }
    solver.solution.methods.discretization_scheme = {"pressure": "presto!"}
    assert solver.solution.methods.discretization_scheme() == {
        "mom": "second-order-upwind",
        "omega": "second-order-upwind",
        "mp": "compressive",
        "pressure": "presto!",
        "k": "second-order-upwind",
        "temperature": "second-order-upwind",
    }
    solver.solution.methods.gradient_scheme = "least-square-cell-based"
    assert solver.solution.methods.gradient_scheme() == "least-square-cell-based"

    enable_warped_face = solver.solution.methods.warped_face_gradient_correction
    enable_warped_face(enable=True, mode="fast")
    enable_warped_face(enable=False, mode="fast")

    solver.solution.methods.expert.numerics_pbns.velocity_formulation = "relative"
    assert (
        solver.solution.methods.expert.numerics_pbns.velocity_formulation()
        == "relative"
    )
    solver.solution.methods.expert.numerics_pbns = {
        "implicit_bodyforce_treatment": True,
        "velocity_formulation": "absolute",
        "physical_velocity_formulation": True,
        "disable_rhie_chow_flux": True,
        "presto_pressure_scheme": False,
        "first_to_second_order_blending": 1.0,
    }
    assert solver.solution.methods.expert.numerics_pbns() == {
        "implicit_bodyforce_treatment": True,
        "velocity_formulation": "absolute",
        "physical_velocity_formulation": True,
        "disable_rhie_chow_flux": True,
        "presto_pressure_scheme": False,
        "first_to_second_order_blending": 1.0,
    }
    solver.solution.methods.expert.numerics_pbns.presto_pressure_scheme = True
    assert solver.solution.methods.expert.numerics_pbns.presto_pressure_scheme() is True
    solver.solution.methods.gradient_scheme = "green-gauss-node-based"
    assert solver.solution.methods.gradient_scheme() == "green-gauss-node-based"
    solver.solution.methods.warped_face_gradient_correction(
        enable=True, mode="memory-saving"
    )
