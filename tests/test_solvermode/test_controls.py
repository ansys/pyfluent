import pytest


@pytest.mark.settings_only
@pytest.mark.fluent_version("latest")
def test_controls(mixing_elbow_settings_session):
    solver = mixing_elbow_settings_session
    solver.setup.models.multiphase.models = "vof"
    assert solver.setup.models.multiphase.models() == "vof"
    solver.setup.general.operating_conditions.gravity = {
        "enable": True,
        "components": [0.0, 0.0, -9.81],
    }
    assert solver.setup.general.operating_conditions.gravity.components() == [
        0,
        0,
        -9.81,
    ]
    solver.setup.general.solver.time = "steady"
    assert solver.setup.general.solver.time() == "steady"
    param_coarsening = (
        solver.solution.controls.advanced.multi_grid.amg_controls.coupled_parameters.coarsening_parameters
    )
    param_coarsening.laplace_coarsening = True
    assert param_coarsening() == {
        "max_coarse_levels": 40,
        "coarsen_by_interval": 8,
        "conservative_coarsening": False,
        "aggressive_coarsening": False,
        "laplace_coarsening": True,
    }
    param_coarsening.max_coarse_levels = 45
    assert param_coarsening.max_coarse_levels() == 45

    param_coarsening.set_state(
        {
            "max_coarse_levels": 48,
            "coarsen_by_interval": 9,
            "conservative_coarsening": True,
            "aggressive_coarsening": True,
            "laplace_coarsening": True,
        }
    )
    assert param_coarsening.max_coarse_levels() == 48
    assert param_coarsening.coarsen_by_interval() == 9
    assert param_coarsening.conservative_coarsening() is True
    assert param_coarsening.aggressive_coarsening() is True

    param_fixed_cycle = (
        solver.solution.controls.advanced.multi_grid.amg_controls.scalar_parameters.fixed_cycle_parameters
    )
    param_fixed_cycle.max_cycle = 300
    assert param_fixed_cycle.max_cycle() == 300
    param_fixed_cycle.set_state(
        {
            "pre_sweeps": 1,
            "post_sweeps": 2,
            "max_cycle": 350,
        }
    )
    assert param_fixed_cycle() == {
        "pre_sweeps": 1,
        "post_sweeps": 2,
        "max_cycle": 350,
    }
    solver.solution.methods.p_v_coupling.flow_scheme = "Coupled"
    assert solver.solution.methods.p_v_coupling.flow_scheme() == "Coupled"
    solver.solution.methods.p_v_coupling.coupled_form = True
    assert solver.solution.methods.p_v_coupling.coupled_form() is True
    solver.solution.controls.advanced.multi_grid.amg_controls.scalar_parameters.smoother_type = (
        "Gauss-Seidel"
    )
    assert (
        solver.solution.controls.advanced.multi_grid.amg_controls.scalar_parameters.smoother_type()
        == "Gauss-Seidel"
    )
    assert solver.solution.controls.pseudo_time_explicit_relaxation_factor() == {
        "global_dt_pseudo_relax": {
            "turb-viscosity": 1.0,
            "body-force": 1.0,
            "k": 0.75,
            "omega": 0.75,
            "mp": 0.5,
            "density": 1.0,
            "temperature": 0.75,
        }
    }
    solver.solution.controls.pseudo_time_explicit_relaxation_factor = {
        "global_dt_pseudo_relax": {"turb-viscosity": 0.9, "body-force": 0.8}
    }
    assert solver.solution.controls.pseudo_time_explicit_relaxation_factor() == {
        "global_dt_pseudo_relax": {
            "turb-viscosity": 0.9,
            "body-force": 0.8,
            "k": 0.75,
            "omega": 0.75,
            "mp": 0.5,
            "density": 1.0,
            "temperature": 0.75,
        }
    }
    solver.solution.methods.p_v_coupling.flow_scheme = "SIMPLE"
    solver.solution.controls.under_relaxation = {"pressure": 0.9}
    solver.solution.controls.under_relaxation = {"density": 0.9}
    assert solver.solution.controls.under_relaxation() == {
        "mom": 0.7,
        "turb-viscosity": 1,
        "density": 0.9,
        "omega": 0.8,
        "mp": 0.5,
        "body-force": 1.0,
        "pressure": 0.9,
        "k": 0.8,
        "temperature": 1.0,
    }
    solver.solution.controls.under_relaxation = {
        "body-force": 0.7,
        "density": 0.75,
        "mom": 0.8,
    }
    assert solver.solution.controls.under_relaxation() == {
        "mom": 0.8,
        "turb-viscosity": 1,
        "density": 0.75,
        "omega": 0.8,
        "mp": 0.5,
        "body-force": 0.7,
        "pressure": 0.9,
        "k": 0.8,
        "temperature": 1.0,
    }
