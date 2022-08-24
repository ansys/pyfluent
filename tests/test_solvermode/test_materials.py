import pytest
from util.solver import copy_database_material


@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
def test_solver_material(load_mixing_elbow_mesh):
    solver_session = load_mixing_elbow_mesh
    copy_database_material(
        materials=solver_session.setup.materials, type="fluid", name="water-liquid"
    )
    assert (
        "water-liquid"
        not in solver_session.setup.cell_zone_conditions.fluid["elbow-fluid"].material()
    )
    solver_session.setup.cell_zone_conditions.fluid[
        "elbow-fluid"
    ].material = "water-liquid"
    assert (
        "water-liquid"
        in solver_session.setup.cell_zone_conditions.fluid["elbow-fluid"].material()
    )
