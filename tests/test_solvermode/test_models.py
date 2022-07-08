import pytest


@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
def test_solver_models(load_mixing_elbow_mesh):
    session = load_mixing_elbow_mesh
    assert not session.solver.root.setup.models.energy.enabled()
    session.solver.root.setup.models.energy.enabled = True
    assert session.solver.root.setup.models.energy.enabled()
