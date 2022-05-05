import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples


def test_setup_models_viscous_model_settings(with_running_pytest) -> None:
    session = pyfluent.launch_fluent()
    root = session.get_settings_root()
    assert root.setup.models.viscous.model() == "laminar"
    assert "inviscid" in root.setup.models.viscous.model.get_attr("allowed-values")
    root.setup.models.viscous.model = "inviscid"
    assert root.setup.models.viscous.model() == "inviscid"


def test_results_graphics_mesh_settings(with_running_pytest) -> None:
    session = pyfluent.launch_fluent()
    case_path = examples.download_file(
        "Static_Mixer_main.cas.h5", "pyfluent/static_mixer"
    )
    root = session.get_settings_root()
    root.file.read(file_type="case", file_name=case_path)
    assert len(root.results.graphics.mesh) == 0
    root.results.graphics.mesh["mesh-1"] = {}
    assert len(root.results.graphics.mesh) == 1
    assert "mesh-1" in root.results.graphics.mesh
    assert not root.results.graphics.mesh["mesh-1"].options.nodes()
    root.results.graphics.mesh["mesh-1"].options.nodes = True
    assert root.results.graphics.mesh["mesh-1"].options.nodes()
    root.results.graphics.mesh.rename("mesh-a", "mesh-1")
    assert "mesh-a" in root.results.graphics.mesh
    assert "mesh-1" not in root.results.graphics.mesh
    del root.results.graphics.mesh["mesh-a"]
    assert "mesh-a" not in root.results.graphics.mesh
    assert len(root.results.graphics.mesh) == 0
