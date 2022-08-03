import pytest


@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
def test_solver_material(load_mixing_elbow_mesh):
    solver_session = load_mixing_elbow_mesh
    solver_session.root.setup.materials.copy_database_material_by_name(
        type="fluid", name="water-liquid"
    )
    assert (
        "water-liquid"
        not in solver_session.root.setup.cell_zone_conditions.fluid[
            "elbow-fluid"
        ].material()
    )
    solver_session.root.setup.cell_zone_conditions.fluid[
        "elbow-fluid"
    ].material = "water-liquid"
    assert (
        "water-liquid"
        in solver_session.root.setup.cell_zone_conditions.fluid[
            "elbow-fluid"
        ].material()
    )
