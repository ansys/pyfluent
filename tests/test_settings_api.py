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
