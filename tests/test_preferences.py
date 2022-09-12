from util.meshing_workflow import new_mesh_session  # noqa: F401
from util.solver_workflow import new_solver_session  # noqa: F401


def test_solver_verbosity(new_solver_session):
    solver = new_solver_session
    solver.preferences.MeshingWorkflow.Verbosity = 10.5
    assert solver.preferences.MeshingWorkflow.Verbosity() == "10.5"
    solver.exit()


def test_meshing_verbosity(new_mesh_session):
    meshing = new_mesh_session
    meshing.preferences.MeshingWorkflow.Verbosity = 15.5
    assert meshing.preferences.MeshingWorkflow.Verbosity() == "15.5"
    meshing.exit()
