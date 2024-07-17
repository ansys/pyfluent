import pytest
from util.solver import copy_database_material


@pytest.mark.settings_only
@pytest.mark.fluent_version("latest")
def test_solver_material(mixing_elbow_settings_session):
    solver_session = mixing_elbow_settings_session
    setup_materials = solver_session.setup.materials
    copy_database_material(materials=setup_materials, type="fluid", name="water-liquid")
    elbow_fluid = solver_session.setup.cell_zone_conditions.fluid["elbow-fluid"]

    assert "water-liquid" not in elbow_fluid.material()
    elbow_fluid.material = "water-liquid"
    assert "water-liquid" in elbow_fluid.material()

    setup_materials.database.copy_by_name(type="fluid", name="air")
    elbow_fluid.material = "air"
    assert "air" in elbow_fluid.material()
    assert "air" in elbow_fluid.material()

    assert setup_materials.child_names == [
        "database",
        "fluid",
        "solid",
        "mixture",
        "inert_particle",
        "droplet_particle",
        "combusting_particle",
        "particle_mixture",
    ]
    assert setup_materials.database.get_active_command_names() == [
        "copy_by_formula",
        "copy_by_name",
        "list_materials",
        "list_properties",
    ]
    setup_materials.database.copy_by_formula(type="fluid", formula="c2h6")
    elbow_fluid.material = "ethane"
    assert "ethane" in elbow_fluid.material()
