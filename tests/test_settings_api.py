import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core.examples import download_file


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.1")
def test_setup_models_viscous_model_settings(new_solver_session) -> None:
    solver_session = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver_session.file.read_case(file_name=case_path)
    solver_session.solution.initialization.hybrid_initialize()

    viscous_model = solver_session.setup.models.viscous

    assert viscous_model.model() == "k-epsilon"
    assert "inviscid" in viscous_model.model.get_attr("allowed-values")
    viscous_model.model = "inviscid"

    assert viscous_model.model() == "inviscid"


@pytest.mark.skip(reason="failing if run with other tests")
def test_results_graphics_mesh_settings(new_solver_session) -> None:
    session = new_solver_session
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    session.solver.file.read(file_type="case", file_name=case_path)
    get_names = session.mesh.get_object_names
    assert "mesh-1" not in get_names()
    session.mesh["mesh-1"] = {}
    assert "mesh-1" in get_names()
    assert not session.mesh["mesh-1"].options.nodes()
    session.mesh["mesh-1"].options.nodes = True
    assert session.mesh["mesh-1"].options.nodes()
    session.mesh.rename("mesh-a", "mesh-1")
    assert "mesh-a" in get_names()
    assert "mesh-1" not in get_names()
    del session.mesh["mesh-a"]
    assert "mesh-a" not in get_names()


@pytest.mark.skip("Fluent bug")
@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.2")
def test_wildcard(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read_case(file_name=case_path)
    boundary_conditions = solver.setup.boundary_conditions
    assert boundary_conditions.velocity_inlet["inl*"].vmag() == {
        "inlet2": {"vmag": {"option": "value", "value": 15}},
        "inlet1": {"vmag": {"option": "value", "value": 5}},
    }
    assert boundary_conditions.velocity_inlet["inl*"].vmag.value() == {
        "inlet2": {"vmag": {"value": 15}},
        "inlet1": {"vmag": {"value": 5}},
    }
    boundary_conditions.velocity_inlet["inl*"].vmag = 10
    assert boundary_conditions.velocity_inlet["inl*"].vmag() == {
        "inlet2": {"vmag": {"option": "value", "value": 10}},
        "inlet1": {"vmag": {"option": "value", "value": 10}},
    }
    boundary_conditions.velocity_inlet = boundary_conditions.velocity_inlet[
        "inl*"
    ].vmag()
    assert boundary_conditions.velocity_inlet["inl*"].vmag() == {
        "inlet2": {"vmag": {"option": "value", "value": 10}},
        "inlet1": {"vmag": {"option": "value", "value": 10}},
    }
    assert boundary_conditions.fluid["*"].source_terms["*mom*"]() == {
        "fluid": {
            "source_terms": {
                "y-momentum": [{"option": "value", "value": 2}],
                "x-momentum": [{"option": "value", "value": 1}],
                "z-momentum": [{"option": "value", "value": 3}],
            }
        }
    }
    boundary_conditions.fluid["*"].source_terms["*mom*"] = [
        {"option": "value", "value": 2}
    ]
    assert solver.setup.cell_zone_conditions.fluid["*"].source_terms["*mom*"]() == {
        "fluid": {
            "source_terms": {
                "x-momentum": [{"option": "value", "value": 2}],
                "y-momentum": [{"option": "value", "value": 2}],
                "z-momentum": [{"option": "value", "value": 2}],
            }
        }
    }


@pytest.mark.skip("Fluent bug")
@pytest.mark.nightly
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


@pytest.mark.nightly
@pytest.mark.fluent_version(">=23.2")
def test_wildcard_path_is_iterable(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read_case(file_name=case_path)

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
