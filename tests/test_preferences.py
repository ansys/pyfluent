from util.meshing_workflow import new_mesh_session  # noqa: F401
from util.solver_workflow import new_solver_session  # noqa: F401


def test_solver_preferences(new_solver_session):
    solver = new_solver_session

    solver.preferences.MeshingWorkflow.Verbosity = 10.5
    assert solver.preferences.MeshingWorkflow.Verbosity() == "10.5"

    solver.preferences.MeshingWorkflow.CheckpointingOption = "Write into memory"
    assert (
        solver.preferences.MeshingWorkflow.CheckpointingOption() == "Write into memory"
    )

    solver.preferences.MeshingWorkflow.DrawSettings.FacetLimit = 6000000
    assert solver.preferences.MeshingWorkflow.DrawSettings.FacetLimit() == 6000000

    solver.preferences.MeshingWorkflow.DrawSettings.FaceZoneLimit = 15000
    solver.preferences.MeshingWorkflow.DrawSettings.FaceZoneLimit() == 15000

    solver.preferences.Appearance.AnsysLogo.Color = "white"
    assert solver.preferences.Appearance.AnsysLogo.Color() == "white"

    solver.preferences.Appearance.AnsysLogo.Color = "black"
    assert solver.preferences.Appearance.AnsysLogo.Color() == "black"

    solver.preferences.Appearance.AnsysLogo.Visible = True
    assert solver.preferences.Appearance.AnsysLogo.Visible() is True

    solver.preferences.Graphics.AnimationOption = "wireframe"
    assert solver.preferences.Graphics.AnimationOption() == "wireframe"

    solver.exit()


def test_meshing_test_solver_preferences(new_mesh_session):
    meshing = new_mesh_session

    meshing.preferences.MeshingWorkflow.Verbosity = 15.5
    assert meshing.preferences.MeshingWorkflow.Verbosity() == "15.5"

    meshing.preferences.MeshingWorkflow.CheckpointingOption = "Write into memory"
    assert (
        meshing.preferences.MeshingWorkflow.CheckpointingOption() == "Write into memory"
    )

    meshing.preferences.MeshingWorkflow.DrawSettings.FacetLimit = 6000000
    assert meshing.preferences.MeshingWorkflow.DrawSettings.FacetLimit() == 6000000

    meshing.preferences.MeshingWorkflow.DrawSettings.FaceZoneLimit = 15000
    meshing.preferences.MeshingWorkflow.DrawSettings.FaceZoneLimit() == 15000

    meshing.preferences.Appearance.AnsysLogo.Color = "white"
    assert meshing.preferences.Appearance.AnsysLogo.Color() == "white"

    meshing.preferences.Appearance.AnsysLogo.Color = "black"
    assert meshing.preferences.Appearance.AnsysLogo.Color() == "black"

    meshing.preferences.Appearance.AnsysLogo.Visible = True
    assert meshing.preferences.Appearance.AnsysLogo.Visible() is True

    meshing.preferences.Graphics.AnimationOption = "wireframe"
    assert meshing.preferences.Graphics.AnimationOption() == "wireframe"

    meshing.exit()
