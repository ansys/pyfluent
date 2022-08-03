import pytest


@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
def test_solver_models(load_mixing_elbow_mesh):
    solver_session = load_mixing_elbow_mesh
    assert not solver_session.root.setup.models.energy.enabled()
    solver_session.root.setup.models.energy.enabled = True
    assert solver_session.root.setup.models.energy.enabled()
