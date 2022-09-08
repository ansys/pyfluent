import ansys.fluent.core as pyfluent


def test_solver_verbosity():
    solver = pyfluent.launch_fluent(mode="solver")
    solver.preferences.MeshingWorkflow.Verbosity = 10.5
    assert solver.preferences.MeshingWorkflow.Verbosity() == "10.5"
    solver.exit()


def test_meshing_verbosity():
    meshing = pyfluent.launch_fluent(mode="meshing")
    meshing.preferences.MeshingWorkflow.Verbosity = 15.5
    assert meshing.preferences.MeshingWorkflow.Verbosity() == "15.5"
    meshing.exit()
