import pytest


@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
def test_solver_models(load_mixing_elbow_mesh):
    solver_session = load_mixing_elbow_mesh
    assert not solver_session.setup.models.energy.enabled()
    solver_session.setup.models.energy.enabled = True
    assert solver_session.setup.models.energy.enabled()


@pytest.mark.quick
@pytest.mark.setup
def test_disk_2d_models(load_disk_mesh):
    session = load_disk_mesh
    solver = session.solver.root
    solver.setup.general.solver.two_dim_space = "axisymmetric"
    solver.setup.general.solver.two_dim_space = "swirl"
    solver.setup.models.viscous.model = "k-epsilon"
    assert solver.setup.models.viscous.model() == "k-epsilon"
    solver.setup.models.viscous.near_wall_treatment.wall_function = (
        "enhanced-wall-treatment"
    )
    assert (
        solver.setup.models.viscous.near_wall_treatment.wall_function()
        == "enhanced-wall-treatment"
    )
    solver.setup.models.viscous.near_wall_treatment.wall_function.get_attr(
        "allowed-values"
    )
    solver.setup.models.viscous.near_wall_treatment.wall_function = "standard-wall-fn"
    assert (
        solver.setup.models.viscous.near_wall_treatment.wall_function()
        == "standard-wall-fn"
    )
    solver.setup.models.viscous.near_wall_treatment.wall_function = (
        "non-equilibrium-wall-fn"
    )
    assert (
        solver.setup.models.viscous.near_wall_treatment.wall_function()
        == "non-equilibrium-wall-fn"
    )
    solver.setup.models.viscous.near_wall_treatment.wall_function = "menter-lechner"
    assert (
        solver.setup.models.viscous.near_wall_treatment.wall_function()
        == "menter-lechner"
    )
    solver.setup.models.viscous.near_wall_treatment.wall_function = (
        "scalable-wall-functions"
    )
    assert (
        solver.setup.models.viscous.near_wall_treatment.wall_function()
        == "scalable-wall-functions"
    )
    solver.setup.models.viscous.near_wall_treatment.wall_function = (
        "user-defined-wall-functions"
    )
    # As udf is not available, so it will change automatically to standard wall function
    assert (
        solver.setup.models.viscous.near_wall_treatment.wall_function()
        == "standard-wall-fn"
    )

    solver.setup.models.viscous.model = "k-omega"
    assert solver.setup.models.viscous.model() == "k-omega"
    assert solver.setup.models.viscous.k_omega_model.get_attr("allowed-values") == [
        "standard",
        "geko",
        "bsl",
        "sst",
    ]
    assert solver.setup.models.viscous.k_omega_model() == "standard"
    solver.setup.models.viscous.k_omega_model = "geko"
    assert solver.setup.models.viscous.k_omega_model() == "geko"
    solver.setup.models.viscous.k_omega_model = "bsl"
    assert solver.setup.models.viscous.k_omega_model() == "bsl"
    solver.setup.models.viscous.k_omega_model = "sst"
    assert solver.setup.models.viscous.k_omega_model() == "sst"
    assert solver.setup.models.viscous.model.get_attr("allowed-values") == [
        "inviscid",
        "laminar",
        "k-epsilon",
        "k-omega",
        "mixing-length",
        "spalart-allmaras",
        "k-kl-w",
        "transition-sst",
        "reynolds-stress",
        "scale-adaptive-simulation",
        "detached-eddy-simulation",
    ]
