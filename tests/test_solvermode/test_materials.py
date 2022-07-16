import pytest


@pytest.mark.integration
@pytest.mark.quick
@pytest.mark.setup
def test_solver_material(load_mixing_elbow_mesh):
    session = load_mixing_elbow_mesh
    session.solver.root.setup.materials.copy_database_material_by_name(
        type="fluid", name="water-liquid"
    )
    assert (
        "water-liquid"
        not in session.solver.root.setup.cell_zone_conditions.fluid[
            "elbow-fluid"
        ].material()
    )
    session.solver.root.setup.cell_zone_conditions.fluid[
        "elbow-fluid"
    ].material = "water-liquid"
    assert (
        "water-liquid"
        in session.solver.root.setup.cell_zone_conditions.fluid[
            "elbow-fluid"
        ].material()
    )
