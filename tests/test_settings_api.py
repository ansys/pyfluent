import pytest
from util.solver_workflow import new_solver_session  # noqa: F401

from ansys.fluent.core.examples import download_file


def test_setup_models_viscous_model_settings(new_solver_session) -> None:
    root = new_solver_session.get_settings_root()
    assert root.setup.models.viscous.model() == "laminar"
    assert "inviscid" in root.setup.models.viscous.model.get_attr("allowed-values")
    root.setup.models.viscous.model = "inviscid"
    assert root.setup.models.viscous.model() == "inviscid"


@pytest.mark.skip(reason="failing if run with other tests")
def test_results_graphics_mesh_settings(new_solver_session) -> None:
    case_path = download_file("Static_Mixer_main.cas.h5", "pyfluent/static_mixer")
    root = new_solver_session.get_settings_root()
    root.file.read(file_type="case", file_name=case_path)
    assert "mesh-1" not in root.results.graphics.mesh.get_object_names()
    root.results.graphics.mesh["mesh-1"] = {}
    assert "mesh-1" in root.results.graphics.mesh.get_object_names()
    assert not root.results.graphics.mesh["mesh-1"].options.nodes()
    root.results.graphics.mesh["mesh-1"].options.nodes = True
    assert root.results.graphics.mesh["mesh-1"].options.nodes()
    root.results.graphics.mesh.rename("mesh-a", "mesh-1")
    assert "mesh-a" in root.results.graphics.mesh.get_object_names()
    assert "mesh-1" not in root.results.graphics.mesh.get_object_names()
    del root.results.graphics.mesh["mesh-a"]
    assert "mesh-a" not in root.results.graphics.mesh.get_object_names()
