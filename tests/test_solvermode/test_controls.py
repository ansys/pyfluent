import pytest


@pytest.mark.nightly
@pytest.mark.quick
@pytest.mark.setup
@pytest.mark.fluent_version(">=23.1")
def test_controls(load_mixing_elbow_mesh):
    solver = load_mixing_elbow_mesh
    solver.setup.models.multiphase.models = "vof"
    assert solver.setup.models.multiphase.models() == "vof"
    solver.setup.general.operating_conditions.gravity = {"enable": True, "components": [0.0, 0.0, -9.81]}
    assert solver.setup.general.operating_conditions.gravity.components() == [0, 0, -9.81]
    solver.setup.general.solver.time = "steady"
    assert solver.setup.general.solver.time() == "steady"
    solver.solution.controls.advanced.multi_grid.amg_controls.coupled_parameters.coarsening_parameters.laplace_coarsening = (
        True
    )
    assert solver.solution.controls.advanced.multi_grid.amg_controls.coupled_parameters.coarsening_parameters() == {
        "max_coarse_levels": 40,
        "coarsen_by_interval": 8,
        "conservative_coarsening": False,
        "aggressive_coarsening": False,
        "laplace_coarsening": True,
    }
    solver.solution.controls.advanced.multi_grid.amg_controls.coupled_parameters.coarsening_parameters.max_coarse_levels = (
        45
    )
    assert (
        solver.solution.controls.advanced.multi_grid.amg_controls.coupled_parameters.coarsening_parameters.max_coarse_levels()
        == 45
    )
    solver.solution.controls.advanced.multi_grid.amg_controls.coupled_parameters.coarsening_parameters = {
        "max_coarse_levels": 48,
        "coarsen_by_interval": 9,
        "conservative_coarsening": True,
        "aggressive_coarsening": True,
        "laplace_coarsening": True,
    }
    assert (
        solver.solution.controls.advanced.multi_grid.amg_controls.coupled_parameters.coarsening_parameters.max_coarse_levels()
        == 48
    )
    assert (
        solver.solution.controls.advanced.multi_grid.amg_controls.coupled_parameters.coarsening_parameters.coarsen_by_interval()
        == 9
    )
    assert (
        solver.solution.controls.advanced.multi_grid.amg_controls.coupled_parameters.coarsening_parameters.conservative_coarsening()
        == True
    )
    assert (
        solver.solution.controls.advanced.multi_grid.amg_controls.coupled_parameters.coarsening_parameters.aggressive_coarsening()
        == True
    )
    solver.solution.controls.advanced.multi_grid.amg_controls.scalar_parameters.fixed_cycle_parameters.max_cycle = (
        300
    )
    assert (
        solver.solution.controls.advanced.multi_grid.amg_controls.scalar_parameters.fixed_cycle_parameters.max_cycle()
        == 300
    )
    solver.solution.controls.advanced.multi_grid.amg_controls.scalar_parameters.fixed_cycle_parameters = {
        "pre_sweeps": 1,
        "post_sweeps": 2,
        "max_cycle": 350,
    }
    assert solver.solution.controls.advanced.multi_grid.amg_controls.scalar_parameters.fixed_cycle_parameters() == {
        "pre_sweeps": 1,
        "post_sweeps": 2,
        "max_cycle": 350,
    }
    solver.solution.methods.p_v_coupling.flow_scheme = "Coupled"
    assert solver.solution.methods.p_v_coupling.flow_scheme() == "Coupled"
    solver.solution.methods.p_v_coupling.coupled_form = True
    assert solver.solution.methods.p_v_coupling.coupled_form() == True
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
    }
