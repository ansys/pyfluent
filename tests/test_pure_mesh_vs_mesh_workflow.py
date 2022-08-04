import pytest


@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
def test_pure_meshing_mode(load_mixing_elbow_pure_meshing):
    pure_meshing_session = load_mixing_elbow_pure_meshing
    assert pure_meshing_session.workflow.TaskObject["Import Geometry"].Execute()
    # throws = False
    with pytest.raises(AttributeError):
        pure_meshing_session.switch_to_solver()

    # try:
    #     pure_meshing_session.switch_to_solver()  # pure-meshing mode does not have this switch
    # except AttributeError:
    #     throws = True
    # assert throws


@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
def test_meshing_mode(load_mixing_elbow_meshing):
    meshing_session = load_mixing_elbow_meshing
    assert meshing_session.workflow.TaskObject["Import Geometry"].Execute()
    assert meshing_session.switch_to_solver()
