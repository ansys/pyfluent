import pytest


def test_pure_meshing_mode(load_mixing_elbow_pure_meshing):
    pure_meshing_session = load_mixing_elbow_pure_meshing
    # check a few dir elements
    # n.b. 'field_data', 'field_info' need to
    # be eliminated from meshing sessions
    session_dir = dir(pure_meshing_session)
    for attr in ("field_data", "field_info", "meshing", "workflow"):
        assert attr in session_dir
    workflow = pure_meshing_session.workflow
    workflow_dir = dir(workflow)
    for attr in ("TaskObject", "InsertNewTask", "Workflow", "setState"):
        assert attr in workflow_dir
    import_geometry = workflow.TaskObject["Import Geometry"]
    import_geometry_dir = dir(import_geometry)
    for attr in ("AddChildToTask", "Arguments", "Execute", "setState"):
        assert attr in import_geometry_dir
    assert import_geometry.Execute()
    with pytest.raises(AttributeError):
        pure_meshing_session.switch_to_solver()


def test_meshing_mode(load_mixing_elbow_meshing):
    meshing_session = load_mixing_elbow_meshing
    # check a few dir elements
    # n.b. 'field_data', 'field_info' need to
    # be eliminated from meshing sessions
    session_dir = dir(meshing_session)
    for attr in ("field_data", "field_info", "meshing", "workflow"):
        assert attr in session_dir
    assert meshing_session.workflow.InitializeWorkflow(
        WorkflowType="Watertight Geometry"
    )
    assert meshing_session.switch_to_solver()


def test_meshing_and_solver_mode_exit(load_mixing_elbow_meshing):
    meshing_session = load_mixing_elbow_meshing
    solver_session = meshing_session.switch_to_solver()
    # Even if exit statement is invoked twice, only one is executed as the channel instance is shared
    meshing_session.exit()
    solver_session.exit()


def test_meshing_mode_post_switching_to_solver(load_mixing_elbow_meshing):
    meshing_session = load_mixing_elbow_meshing
    meshing_session.switch_to_solver()
    # Post switching to solver session, meshing session specific attributes are unavailable
    with pytest.raises(AttributeError):
        meshing_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
