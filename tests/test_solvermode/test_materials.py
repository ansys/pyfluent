import pytest
from util.solver import copy_database_material


@pytest.mark.nightly
@pytest.mark.quick
@pytest.mark.setup
@pytest.mark.fluent_version(">=23.1")
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

    solver_session.setup.materials.database.copy_by_name(type="fluid", name="air")
    solver_session.setup.cell_zone_conditions.fluid["elbow-fluid"].material = "air"
    assert (
        "air"
        in solver_session.setup.cell_zone_conditions.fluid["elbow-fluid"].material()
    )
    assert (
        "air"
        in solver_session.setup.cell_zone_conditions.fluid["elbow-fluid"].material()
    )
    assert solver_session.setup.materials.child_names == [
        "database",
        "fluid",
        "solid",
        "mixture",
        "inert_particle",
        "droplet_particle",
        "combusting_particle",
        "particle_mixture",
    ]
    assert solver_session.setup.materials.database.get_active_command_names() == [
        "copy_by_formula",
        "copy_by_name",
        "list_materials",
        "list_properties",
    ]

    solver_session.setup.materials.database.copy_by_formula(
        type="fluid", formula="c2h6"
    )

    solver_session.setup.cell_zone_conditions.fluid["elbow-fluid"].material = "ethane"
    assert (
        "ethane"
        in solver_session.setup.cell_zone_conditions.fluid["elbow-fluid"].material()
    )
