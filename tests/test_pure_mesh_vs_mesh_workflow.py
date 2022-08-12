import pytest


@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
def test_pure_meshing_mode(load_mixing_elbow_pure_meshing):
    pure_meshing_session = load_mixing_elbow_pure_meshing
    assert pure_meshing_session.workflow.TaskObject["Import Geometry"].Execute()
    with pytest.raises(AttributeError):
        pure_meshing_session.switch_to_solver()


@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
def test_meshing_mode(load_mixing_elbow_meshing):
    meshing_session = load_mixing_elbow_meshing
    assert meshing_session.workflow.TaskObject["Import Geometry"].Execute()
    assert meshing_session.switch_to_solver()


@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
def test_meshing_and_solver_mode_exit(load_mixing_elbow_meshing):
    meshing_session = load_mixing_elbow_meshing
    solver_session = meshing_session.switch_to_solver()
    # Even if exit statement is invoked twice, only one is executed as the channel instance is shared
    meshing_session.exit()
    solver_session.exit()


@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
def test_meshing_mode_post_switching_to_solver(load_mixing_elbow_meshing):
    meshing_session = load_mixing_elbow_meshing
    meshing_session.switch_to_solver()
    # Post switching to solver session, meshing session specific attributes are unavailable
    # with pytest.raises(AttributeError):
    #    meshing_session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
