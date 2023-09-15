import pytest
from util.meshing_workflow import new_mesh_session  # noqa: F401
from util.solver_workflow import new_solver_session  # noqa: F401


@pytest.mark.codegen_required
def test_solver_preferences(new_solver_session):
    solver = new_solver_session
    prefered_meshing = solver.preferences.MeshingWorkflow
    prefered_meshing.Verbosity = "off"
    assert prefered_meshing.Verbosity() == "off"

    prefered_meshing.CheckpointingOption = "Write into memory"
    assert prefered_meshing.CheckpointingOption() == "Write into memory"

    prefered_drawing = prefered_drawing
    prefered_drawing.FacetLimit = 6000000
    assert prefered_drawing.FacetLimit() == 6000000
    prefered_drawing.FaceZoneLimit = 15000
    prefered_drawing.FaceZoneLimit() == 15000

    ansys_logo = solver.preferences.Appearance.AnsysLogo
    ansys_logo.Color = "white"
    assert ansys_logo.Color() == "white"

    ansys_logo.Color = "black"
    assert ansys_logo.Color() == "black"

    ansys_logo.Visible = True
    assert ansys_logo.Visible() is True

    perfered_graphics = solver.preferences.Graphics
    perfered_graphics.AnimationOption = "wireframe"
    assert perfered_graphics.AnimationOption() == "wireframe"

    solver.exit()


@pytest.mark.codegen_required
def test_meshing_preferences(new_mesh_session):
    meshing = new_mesh_session
    prefered_meshing = meshing.preferences.MeshingWorkflow
    prefered_meshing.Verbosity = "off"
    assert prefered_meshing.Verbosity() == "off"

    prefered_meshing.CheckpointingOption = "Write into memory"
    assert prefered_meshing.CheckpointingOption() == "Write into memory"

    prefered_drawing = prefered_meshing.DrawSettings
    prefered_drawing.FacetLimit = 6000000
    assert prefered_drawing.FacetLimit() == 6000000

    prefered_drawing.FaceZoneLimit = 15000
    prefered_drawing.FaceZoneLimit() == 15000

    ansys_logo = meshing.preferences.Appearance.AnsysLogo
    ansys_logo.Color = "white"
    assert ansys_logo.Color() == "white"

    ansys_logo.Color = "black"
    assert ansys_logo.Color() == "black"

    ansys_logo.Visible = True
    assert ansys_logo.Visible() is True

    prefered_graphics = meshing.preferences.Graphics
    prefered_graphics.AnimationOption = "wireframe"
    assert prefered_graphics.AnimationOption() == "wireframe"

    meshing.exit()
