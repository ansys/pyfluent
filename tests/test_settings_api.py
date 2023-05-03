import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core.examples import download_file


@pytest.mark.dev
@pytest.mark.fluent_231
@pytest.mark.fluent_232
def test_setup_models_viscous_model_settings(new_solver_session) -> None:
    solver_session = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver_session.file.read_case(file_name=case_path)
    solver_session.solution.initialization.hybrid_initialize()
    assert solver_session.setup.models.viscous.model() == "k-epsilon"
    assert "inviscid" in solver_session.setup.models.viscous.model.get_attr(
        "allowed-values"
    )
    solver_session.setup.models.viscous.model = "inviscid"
    assert solver_session.setup.models.viscous.model() == "inviscid"


@pytest.mark.skip(reason="failing if run with other tests")
def test_results_graphics_mesh_settings(new_solver_session) -> None:
    session = new_solver_session
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    session.solver.file.read(file_type="case", file_name=case_path)
    assert "mesh-1" not in session.solver.results.graphics.mesh.get_object_names()
    session.solver.results.graphics.mesh["mesh-1"] = {}
    assert "mesh-1" in session.solver.results.graphics.mesh.get_object_names()
    assert not session.solver.results.graphics.mesh["mesh-1"].options.nodes()
    session.solver.results.graphics.mesh["mesh-1"].options.nodes = True
    assert session.solver.results.graphics.mesh["mesh-1"].options.nodes()
    session.solver.results.graphics.mesh.rename("mesh-a", "mesh-1")
    assert "mesh-a" in session.solver.results.graphics.mesh.get_object_names()
    assert "mesh-1" not in session.solver.results.graphics.mesh.get_object_names()
    del session.solver.results.graphics.mesh["mesh-a"]
    assert "mesh-a" not in session.solver.results.graphics.mesh.get_object_names()


@pytest.mark.dev
@pytest.mark.fluent_232
def test_wildcard(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read_case(file_name=case_path)
    assert solver.setup.boundary_conditions.velocity_inlet["inl*"].vmag() == {
        "inlet2": {"vmag": {"option": "value", "value": 15}},
        "inlet1": {"vmag": {"option": "value", "value": 5}},
    }
    assert solver.setup.boundary_conditions.velocity_inlet["inl*"].vmag.value() == {
        "inlet2": {"vmag": {"value": 15}},
        "inlet1": {"vmag": {"value": 5}},
    }
    solver.setup.boundary_conditions.velocity_inlet["inl*"].vmag = 10
    assert solver.setup.boundary_conditions.velocity_inlet["inl*"].vmag() == {
        "inlet2": {"vmag": {"option": "value", "value": 10}},
        "inlet1": {"vmag": {"option": "value", "value": 10}},
    }
    solver.setup.boundary_conditions.velocity_inlet = (
        solver.setup.boundary_conditions.velocity_inlet["inl*"].vmag()
    )
    assert solver.setup.boundary_conditions.velocity_inlet["inl*"].vmag() == {
        "inlet2": {"vmag": {"option": "value", "value": 10}},
        "inlet1": {"vmag": {"option": "value", "value": 10}},
    }
    assert solver.setup.cell_zone_conditions.fluid["*"].source_terms["*mom*"]() == {
        "fluid": {
            "source_terms": {
                "y-momentum": [{"option": "value", "value": 2}],
                "x-momentum": [{"option": "value", "value": 1}],
                "z-momentum": [{"option": "value", "value": 3}],
            }
        }
    }
    solver.setup.cell_zone_conditions.fluid["*"].source_terms["*mom*"] = [
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


@pytest.mark.dev
@pytest.mark.fluent_232
def test_wildcard_fnmatch(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read_case(file_name=case_path)

    solver.solution.initialization.hybrid_initialize()

    solver.results.graphics.mesh.create("mesh-2")
    solver.results.graphics.mesh.create("mesh-a")
    solver.results.graphics.mesh.create("mesh-bc")

    assert (
        list(solver.results.graphics.mesh["mesh-*"]().keys()).sort()
        == ["mesh-1", "mesh-2", "mesh-a", "mesh-bc"].sort()
    )

    assert list(solver.results.graphics.mesh["mesh-?c"]().keys()) == ["mesh-bc"]

    assert list(solver.results.graphics.mesh["mesh-[2-5]"]().keys()) == ["mesh-2"]

    assert (
        list(solver.results.graphics.mesh["mesh-[!2-5]"]().keys()).sort()
        == ["mesh-1", "mesh-a"].sort()
    )


@pytest.mark.dev
@pytest.mark.fluent_232
def test_wildcard_path_is_iterable(new_solver_session):
    solver = new_solver_session
    case_path = download_file("elbow_source_terms.cas.h5", "pyfluent/mixing_elbow")
    solver.file.read_case(file_name=case_path)

    assert [x for x in solver.setup.boundary_conditions.velocity_inlet] == [
        "inlet2",
        "inlet1",
    ]

    assert [x for x in solver.setup.boundary_conditions.velocity_inlet["*let*"]] == [
        "inlet2",
        "inlet1",
    ]

    assert [x for x in solver.setup.boundary_conditions.velocity_inlet["*1*"]] == [
        "inlet1"
    ]

    test_data = []
    for k, v in solver.setup.boundary_conditions.velocity_inlet.items():
        test_data.append((k, v))

    assert test_data[0][0] == "inlet2"
    assert test_data[0][1].path == r"setup/boundary-conditions/velocity-inlet/inlet2"
    assert test_data[1][0] == "inlet1"
    assert test_data[1][1].path == r"setup/boundary-conditions/velocity-inlet/inlet1"

    test_data = []
    for k, v in solver.setup.boundary_conditions.velocity_inlet["*let*"].items():
        test_data.append((k, v))

    assert test_data[0][0] == "inlet2"
    assert test_data[0][1].path == r"setup/boundary-conditions/velocity-inlet/inlet2"
    assert test_data[1][0] == "inlet1"
    assert test_data[1][1].path == r"setup/boundary-conditions/velocity-inlet/inlet1"
