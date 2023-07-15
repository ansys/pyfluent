import pytest


@pytest.mark.nightly
@pytest.mark.quick
@pytest.mark.setup
@pytest.mark.fluent_version(">=23.1")
def test_methods(load_mixing_elbow_mesh):
    solver = load_mixing_elbow_mesh
    solver.setup.models.multiphase.models = "vof"
    solver.setup.general.gravity = {"enable": True, "components": [0.0, 0.0, -9.81]}
    solver.setup.general.solver.time = "steady"
    solver.solution.methods.p_v_coupling.flow_scheme = "Coupled"
    solver.solution.methods.p_v_coupling.coupled_form = False
    assert solver.solution.methods.p_v_coupling() == {
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
    }
    solver.solution.methods.gradient_scheme = "least-square-cell-based"
    assert solver.solution.methods.gradient_scheme() == "least-square-cell-based"
    solver.solution.methods.warped_face_gradient_correction.enable(
        enable=True, gradient_correction_mode="fast-mode"
    )
    solver.solution.methods.warped_face_gradient_correction.enable(
        enable=False, gradient_correction_mode="fast-mode"
    )
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
        "first_to_second_order_blending": 2.0,
    }
    assert solver.solution.methods.expert.numerics_pbns() == {
        "implicit_bodyforce_treatment": True,
        "velocity_formulation": "absolute",
        "physical_velocity_formulation": True,
        "disable_rhie_chow_flux": True,
        "presto_pressure_scheme": False,
        "first_to_second_order_blending": 2.0,
    }
    solver.solution.methods.expert.numerics_pbns.presto_pressure_scheme = True
    assert solver.solution.methods.expert.numerics_pbns.presto_pressure_scheme() == True
    solver.solution.methods.gradient_scheme = "green-gauss-node-based"
    assert solver.solution.methods.gradient_scheme() == "green-gauss-node-based"
    solver.solution.methods.warped_face_gradient_correction.enable(
        enable=True, gradient_correction_mode="memory-saving-mode"
    )
