import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core.examples import download_file
from ansys.fluent.core.solver.flobject import (
    DeprecatedSettingWarning,
    UnstableSettingWarning,
    _Alias,
)
from ansys.fluent.core.utils.fluent_version import FluentVersion


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.1")
def test_setup_models_viscous_model_settings(new_solver_session) -> None:
    solver_session = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver_session.file.read(
        file_name=case_path, file_type="case", lightweight_setup=True
    )
    # NOTE: Not sure why initialization is necessary here
    # solver_session.solution.initialization.hybrid_initialize()

    viscous_model = solver_session.setup.models.viscous

    assert viscous_model.model() == "k-epsilon"
    assert "inviscid" in viscous_model.model.get_attr("allowed-values")
    viscous_model.model = "inviscid"

    assert viscous_model.model() == "inviscid"


@pytest.mark.fluent_version(">=24.1")
def test_wildcard(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read(file_name=case_path, file_type="case", lightweight_setup=True)
    boundary_conditions = solver.setup.boundary_conditions
    assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity() == {
        "inlet2": {"momentum": {"velocity": {"option": "value", "value": 15}}},
        "inlet1": {"momentum": {"velocity": {"option": "value", "value": 5}}},
    }
    assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity.value() == {
        "inlet2": {"momentum": {"velocity": {"value": 15}}},
        "inlet1": {"momentum": {"velocity": {"value": 5}}},
    }
    boundary_conditions.velocity_inlet["inl*"].momentum.velocity = 10
    assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity() == {
        "inlet2": {"momentum": {"velocity": {"option": "value", "value": 10}}},
        "inlet1": {"momentum": {"velocity": {"option": "value", "value": 10}}},
    }
    boundary_conditions.velocity_inlet = boundary_conditions.velocity_inlet[
        "inl*"
    ].momentum.velocity()
    assert boundary_conditions.velocity_inlet["inl*"].momentum.velocity() == {
        "inlet2": {"momentum": {"velocity": {"option": "value", "value": 10}}},
        "inlet1": {"momentum": {"velocity": {"option": "value", "value": 10}}},
    }
    cell_zone_conditions = solver.setup.cell_zone_conditions
    if solver.get_fluent_version() >= FluentVersion.v242:
        sources = cell_zone_conditions.fluid["*"].source_terms.sources
        key = "sources"
    else:
        sources = cell_zone_conditions.fluid["*"].source_terms.source_terms
        key = "source_terms"
    assert sources["*mom*"]() == {
        "fluid": {
            "source_terms": {
                key: {
                    "x-momentum": [{"option": "value", "value": 1}],
                    "y-momentum": [{"option": "value", "value": 2}],
                    "z-momentum": [{"option": "value", "value": 3}],
                }
            }
        }
    }
    sources["*mom*"] = [{"option": "value", "value": 2}]
    assert sources["*mom*"]() == {
        "fluid": {
            "source_terms": {
                key: {
                    "x-momentum": [{"option": "value", "value": 2}],
                    "y-momentum": [{"option": "value", "value": 2}],
                    "z-momentum": [{"option": "value", "value": 2}],
                }
            }
        }
    }

    with pytest.raises(AttributeError):
        boundary_conditions.velocity_inlet["inl*"].moment


@pytest.mark.fluent_version(">=23.2")
def test_wildcard_fnmatch(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read_case(file_name=case_path)

    solver.solution.initialization.hybrid_initialize()

    mesh = solver.results.graphics.mesh
    mesh.create("mesh-2")
    mesh.create("mesh-a")
    mesh.create("mesh-bc")

    assert sorted(mesh["mesh-*"]()) == sorted(["mesh-1", "mesh-2", "mesh-a", "mesh-bc"])

    assert list(mesh["mesh-?c"]().keys()) == ["mesh-bc"]

    assert list(mesh["mesh-[2-5]"]().keys()) == ["mesh-2"]

    assert sorted(mesh["mesh-[!2-5]"]()) == sorted(["mesh-1", "mesh-a"])


@pytest.mark.fluent_version(">=23.2")
def test_wildcard_path_is_iterable(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read(file_name=case_path, file_type="case", lightweight_setup=True)

    velocity_inlet = solver.setup.boundary_conditions.velocity_inlet
    assert [x for x in velocity_inlet] == ["inlet2", "inlet1"]
    assert [x for x in velocity_inlet["*let*"]] == ["inlet2", "inlet1"]
    assert [x for x in velocity_inlet["*1*"]] == ["inlet1"]

    test_data = []
    for k, v in velocity_inlet.items():
        test_data.append((k, v))

    assert test_data[0][0] == "inlet2"
    assert test_data[0][1].path == r"setup/boundary-conditions/velocity-inlet/inlet2"
    assert test_data[1][0] == "inlet1"
    assert test_data[1][1].path == r"setup/boundary-conditions/velocity-inlet/inlet1"

    test_data = []
    for k, v in velocity_inlet["*let*"].items():
        test_data.append((k, v))

    assert test_data[0][0] == "inlet2"
    assert test_data[0][1].path == r"setup/boundary-conditions/velocity-inlet/inlet2"
    assert test_data[1][0] == "inlet1"
    assert test_data[1][1].path == r"setup/boundary-conditions/velocity-inlet/inlet1"


@pytest.mark.fluent_version(">=23.1")
def test_api_upgrade(new_solver_session, capsys):
    solver = new_solver_session
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    solver.tui.file.read_case(case_path)
    "<solver_session>.file.read_case" in capsys.readouterr().out


@pytest.mark.fluent_version(">=24.2")
def test_deprecated_settings(new_solver_session):
    solver = new_solver_session
    case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
    solver.file._setattr("_child_aliases", {"rcd": "read_case_data"})
    with pytest.warns(DeprecatedSettingWarning):
        solver.file.rcd(file_name=case_path)

    solver.setup.boundary_conditions.velocity_inlet.child_object_type._child_aliases[
        "mom"
    ] = "momentum"
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.velocity_inlet["hot-inlet"].mom.velocity = 20
    assert (
        solver.setup.boundary_conditions.velocity_inlet[
            "hot-inlet"
        ].momentum.velocity.value()
        == 20
    )
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.velocity_inlet["cold-inlet"].mom.velocity = 2
    assert (
        solver.setup.boundary_conditions.velocity_inlet[
            "cold-inlet"
        ].momentum.velocity.value()
        == 2
    )

    solver.setup.boundary_conditions.wall["wall-inlet"].thermal.thermal_bc = (
        "Temperature"
    )
    assert (
        len(
            solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t._child_aliases
        )
        > 0
    )
    assert (
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t._child_aliases[
            "constant"
        ]
        == "value"
    )
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t.constant = 400

    assert solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t.value() == 400
    assert (
        len(
            solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t._child_aliases
        )
        > 0
    )
    assert isinstance(
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t._child_alias_objs[
            "constant"
        ],
        _Alias,
    )
    solver.setup.boundary_conditions.wall["wall-inlet"].thermal._setattr(
        "_child_aliases", {"temp": "t"}
    )
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.temp.value = 410

    assert solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t.value() == 410

    solver.setup.boundary_conditions._setattr("_child_aliases", {"w": "wall"})
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.w["wall-inlet"].thermal.t.value = 420

    assert solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t.value() == 420

    solver.setup._setattr("_child_aliases", {"bc": "boundary_conditions"})
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.bc.wall["wall-inlet"].thermal.t.value = 430

    assert solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t.value() == 430

    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t.constant = 400

    assert solver.setup.boundary_conditions.wall["wall-inlet"].thermal.t.value() == 400

    solver.results._setattr("_child_aliases", {"gr": "graphics"})
    with pytest.warns(DeprecatedSettingWarning):
        solver.results.gr.contour.create("c1")

    with pytest.warns(DeprecatedSettingWarning):
        solver.results.gr.contour["c1"].field = "pressure"

    assert solver.results.graphics.contour["c1"].field() == "pressure"

    with pytest.warns(DeprecatedSettingWarning):
        del solver.results.gr.contour["c1"]

    assert "c1" not in solver.results.graphics.contour

    solver.setup.boundary_conditions.velocity_inlet[
        "hot-inlet"
    ].momentum.velocity._child_aliases["hd"] = "../../turbulence/hydraulic_diameter"
    with pytest.warns(DeprecatedSettingWarning):
        solver.setup.boundary_conditions.velocity_inlet[
            "hot-inlet"
        ].momentum.velocity.hd = 10
    assert (
        solver.setup.boundary_conditions.velocity_inlet[
            "hot-inlet"
        ].turbulence.hydraulic_diameter()
        == 10
    )

    solver.setup.cell_zone_conditions.fluid["elbow-fluid"] = {"material": "air"}


@pytest.mark.fluent_version(">=24.2")
def test_command_return_type(new_solver_session):
    solver = new_solver_session
    case_path = download_file("mixing_elbow.cas.h5", "pyfluent/mixing_elbow")
    download_file("mixing_elbow.dat.h5", "pyfluent/mixing_elbow")
    ret = solver.file.read_case_data(file_name=case_path)
    assert ret is None
    solver.solution.report_definitions.surface["surface-1"] = dict(
        surface_names=["cold-inlet"]
    )
    ret = solver.solution.report_definitions.compute(report_defs=["surface-1"])
    assert ret is not None


@pytest.mark.fluent_version(">=24.2")
def test_unstable_settings_warning(new_solver_session, recwarn):
    solver = new_solver_session
    solver.file.export
    assert len(recwarn) == 1
    assert recwarn.pop().category == UnstableSettingWarning
    try:
        solver.file.exp
    except AttributeError:
        pass
    assert len(recwarn) == 0
    solver.file.export
    assert len(recwarn) == 1
    assert recwarn.pop().category == UnstableSettingWarning
