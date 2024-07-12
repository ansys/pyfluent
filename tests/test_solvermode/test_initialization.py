import pytest

from ansys.fluent.core.examples.downloads import download_file


@pytest.mark.settings_only
def test_initialization_settings(new_solver_session):
    solver = new_solver_session
    case_name = download_file(
        "wigley.cas.h5",
        "pyfluent/wigley_hull",
    )
    solver.file.read(
        file_type="case",
        file_name=case_name,
        lightweight_setup=True,
    )
    solver.parallel.partition.set.laplace_smoothing.enabled = True
    solver.parallel.partition.method(partition_method="metis", count=2)
    copy_by_name = solver.setup.materials.database.copy_by_name
    copy_by_name(type="fluid", name="air")
    copy_by_name(type="fluid", name="water-liquid")
    solver.setup.models.multiphase.models = "vof"
    solver.setup.general.operating_conditions.gravity = {
        "enable": True,
        "components": [0.0, 0.0, -9.81],
    }
    solver.setup.general.solver.time = "steady"

    solver.tui.define.models.multiphase.vof_sub_models("yes", "no")
    solver.tui.define.phases.set_domain_properties.change_phases_names("water", "air")
    solver.setup.boundary_conditions.pressure_inlet["inflow"].phase["mixture"] = {
        "multiphase": {
            "open_channel": True,
            "vmag": 1.452,
            "ht_bottom": -0.941875,
        },
        "momentum": {"direction_specification_method": "Direction Vector"},
        "turbulence": {
            "turbulent_intensity": 0.01,
            "turbulent_viscosity_ratio": 1,
        },
    }
    solver.setup.boundary_conditions.pressure_outlet["outflow"].phase["mixture"] = {
        "multiphase": {
            "open_channel": True,
            "ht_bottom": -0.941875,
            "den_spec": "From Free Surface Level",
        },
        "momentum": {
            "direction_spec": "Normal to Boundary",
            "p_backflow_spec_gen": "Static Pressure",
        },
        "turbulence": {
            "turbulent_intensity": 0.01,
            "turbulent_viscosity_ratio": 1,
        },
    }

    solver.solution.methods.p_v_coupling.flow_scheme = "Coupled"
    solver.solution.methods.p_v_coupling.coupled_form = True
    solver.solution.controls.advanced.multi_grid.amg_controls.coupled_parameters.coarsening_parameters.laplace_coarsening = (
        True
    )
    solver.solution.initialization.open_channel_auto_init = {
        "boundary_zone": 3,
        "flat_init": True,
    }
    assert solver.solution.initialization.open_channel_auto_init() == {
        "boundary_zone": 3,
        "flat_init": True,
    }


@pytest.mark.fluent_version(">=24.1")
def test_fmg_initialize(new_solver_session):
    solver = new_solver_session
    case_name = download_file("vki_turbine.cas.gz", "pyfluent/vki_turbine")
    solver.file.read(file_type="case", file_name=case_name)
    solver.mesh.check()
    solver.solution.initialization.standard_initialize()
    solver.solution.initialization.fmg.fmg_initialize()
    solver.tui.solve.iterate(2)
