import pytest


@pytest.mark.nightly
@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
@pytest.mark.fluent_version(">=23.1")
def test_solver_models(load_mixing_elbow_mesh):
    solver_session = load_mixing_elbow_mesh
    assert not solver_session.setup.models.energy.enabled()
    solver_session.setup.models.energy.enabled = True
    assert solver_session.setup.models.energy.enabled()
    solver_session.setup.models.multiphase.models = "vof"
    assert solver_session.setup.models.multiphase.models() == "vof"
    solver_session.setup.models.viscous.model = "laminar"
    assert solver_session.setup.models.viscous.model() == "laminar"
    solver_session.setup.models.viscous.model = "k-epsilon"
    assert solver_session.setup.models.viscous.model() == "k-epsilon"
    solver_session.setup.models.viscous.near_wall_treatment.wall_function = (
        "enhanced-wall-treatment"
    )
    solver_session.setup.models.multiphase.models = "eulerian"
    assert solver_session.setup.models.multiphase.models() == "eulerian"


@pytest.mark.nightly
@pytest.mark.quick
@pytest.mark.setup
@pytest.mark.fluent_version(">=23.1")
def test_disk_2d_models(load_disk_mesh):
    solver_session = load_disk_mesh
    solver_session.setup.general.solver.two_dim_space = "axisymmetric"
    solver_session.setup.general.solver.two_dim_space = "swirl"
    solver_session.setup.models.viscous.model = "k-epsilon"
    assert solver_session.setup.models.viscous.model() == "k-epsilon"
    solver_session.setup.models.viscous.near_wall_treatment.wall_function = (
        "enhanced-wall-treatment"
    )
    assert (
        solver_session.setup.models.viscous.near_wall_treatment.wall_function()
        == "enhanced-wall-treatment"
    )
    solver_session.setup.models.viscous.near_wall_treatment.wall_function.get_attr(
        "allowed-values"
    )
    solver_session.setup.models.viscous.near_wall_treatment.wall_function = (
        "standard-wall-fn"
    )
    assert (
        solver_session.setup.models.viscous.near_wall_treatment.wall_function()
        == "standard-wall-fn"
    )

    solver_session.setup.models.viscous.near_wall_treatment.wall_function = (
        "non-equilibrium-wall-fn"
    )
    assert (
        solver_session.setup.models.viscous.near_wall_treatment.wall_function()
        == "non-equilibrium-wall-fn"
    )
    solver_session.setup.models.viscous.near_wall_treatment.wall_function = (
        "menter-lechner"
    )
    assert (
        solver_session.setup.models.viscous.near_wall_treatment.wall_function()
        == "menter-lechner"
    )
    solver_session.setup.models.viscous.near_wall_treatment.wall_function = (
        "scalable-wall-functions"
    )
    assert (
        solver_session.setup.models.viscous.near_wall_treatment.wall_function()
        == "scalable-wall-functions"
    )
    solver_session.setup.models.viscous.near_wall_treatment.wall_function = (
        "user-defined-wall-functions"
    )
    # As udf is not available, so it will change automatically to standard wall function
    assert (
        solver_session.setup.models.viscous.near_wall_treatment.wall_function()
        == "standard-wall-fn"
    )

    solver_session.setup.models.viscous.model = "k-omega"
    assert solver_session.setup.models.viscous.model() == "k-omega"
    assert solver_session.setup.models.viscous.k_omega_model.get_attr(
        "allowed-values"
    ) == [
        "standard",
        "geko",
        "bsl",
        "sst",
    ]
    assert solver_session.setup.models.viscous.k_omega_model() == "standard"
    solver_session.setup.models.viscous.k_omega_model = "geko"
    assert solver_session.setup.models.viscous.k_omega_model() == "geko"
    solver_session.setup.models.viscous.k_omega_model = "bsl"
    assert solver_session.setup.models.viscous.k_omega_model() == "bsl"
    solver_session.setup.models.viscous.k_omega_model = "sst"
    assert solver_session.setup.models.viscous.k_omega_model() == "sst"
    assert solver_session.setup.models.viscous.model.get_attr("allowed-values") == [
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
    solver_session.setup.models.viscous.k_omega_options.kw_low_re_correction = True
    assert (
        solver_session.setup.models.viscous.k_omega_options.kw_low_re_correction()
        == True
    )
    solver_session.setup.models.viscous.turbulence_expert.kato_launder_model = True
    assert (
        solver_session.setup.models.viscous.turbulence_expert.kato_launder_model()
        == True
    )

    solver_session.setup.models.viscous.turbulence_expert.production_limiter.clip_factor = (
        9
    )
    assert (
        solver_session.setup.models.viscous.turbulence_expert.production_limiter.clip_factor()
        == 9
    )
    solver_session.setup.models.viscous.turbulence_expert.turb_non_newtonian = True
    assert (
        solver_session.setup.models.viscous.turbulence_expert.turb_non_newtonian()
        == True
    )
    solver_session.setup.models.viscous.model = "laminar"
    assert solver_session.setup.models.viscous.model() == "laminar"
    solver_session.setup.models.viscous.model = "spalart-allmaras"
    assert solver_session.setup.models.viscous.model() == "spalart-allmaras"
