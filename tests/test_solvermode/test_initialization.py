import pytest
from util.fixture_fluent import download_input_file


@pytest.mark.nightly
@pytest.mark.quick
@pytest.mark.setup
@pytest.mark.fluent_version(">=23.2")
def test_initialize(launch_fluent_solver_3ddp_t2):
    solver = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file("pyfluent/wigley_hull", "wigley.msh")
    solver.file.read(file_type=input_type, file_name=input_name)
    solver.parallel.partition.set.laplace_smoothing.enabled = True
    solver.parallel.partition.method(partition_method="metis", count=2)
    solver.setup.materials.database.copy_by_name(type="fluid", name="air")
    solver.setup.materials.database.copy_by_name(type="fluid", name="water-liquid")
    solver.setup.models.multiphase.models = "vof"
    solver.setup.general.operating_conditions.gravity = {
        "enable": True,
        "components": [0.0, 0.0, -9.81],
    }
    solver.setup.general.solver.time = "steady"

    solver.tui.define.models.multiphase.vof_sub_models("yes", "no")
    solver.tui.define.phases.set_domain_properties.change_phases_names("water", "air")
    solver.setup.boundary_conditions.pressure_inlet["inflow"].phase["mixture"] = {
        "open_channel": True,
        "direction_spec": "Direction Vector",
        "vmag": 1.452,
        "ht_bottom": -0.941875,
        "turb_intensity": 0.01,
        "turb_viscosity_ratio": 1,
    }
    solver.setup.boundary_conditions.pressure_outlet["outflow"].phase["mixture"] = {
        "open_channel": True,
        "ht_bottom": -0.941875,
        "den_spec": "From Free Surface Level",
        "direction_spec": "Normal to Boundary",
        "turb_intensity": 0.01,
        "turb_viscosity_ratio": 1,
        "p_backflow_spec_gen": "Static Pressure",
    }

    solver.solution.methods.p_v_coupling.flow_scheme = "Coupled"
    solver.solution.methods.p_v_coupling.coupled_form = True
    solver.solution.controls.advanced.multi_grid.amg_controls.coupled_parameters.coarsening_parameters.laplace_coarsening = (
        True
    )
    solver.solution.initialization.open_channel_auto_init = {
        "boundary_thread": 3,
        "flat_init": True,
    }
    assert solver.solution.initialization.open_channel_auto_init() == {
        "boundary_thread": 3,
        "flat_init": True,
    }
    # solver.solution.initialization.hybrid_initialize()
    # solver.exit()


@pytest.mark.nightly
@pytest.mark.quick
@pytest.mark.setup
@pytest.mark.fluent_version(">=23.1")
def test_fmg_initialize(launch_fluent_solver_3ddp_t2):
    solver = launch_fluent_solver_3ddp_t2
    input_type, input_name = download_input_file(
        "pyfluent/vki_turbine", "vki_turbine.cas.gz"
    )
    solver.file.read(file_type=input_type, file_name=input_name)
    solver.mesh.check()
    solver.solution.initialization.standard_initialize()
    solver.solution.initialization.fmg_initialize()
    # assert solver.solution.initialization.fmg_initialize() == True
    solver.tui.solve.iterate(2)
    # solver.solution.initialization.hybrid_initialize()
