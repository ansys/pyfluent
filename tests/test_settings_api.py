import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core.examples import download_file


def test_setup_models_viscous_model_settings(new_solver_session) -> None:
    solver_session = new_solver_session
    assert solver_session.setup.models.viscous.model() == "laminar"
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
