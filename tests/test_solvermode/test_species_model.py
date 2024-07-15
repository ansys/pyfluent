import pytest


@pytest.mark.settings_only
@pytest.mark.fluent_version(">=24.1")
def test_change_create_mixture(mixing_elbow_settings_session):
    solver_session = mixing_elbow_settings_session

    # Test turning on species transport model
    species_mdl = solver_session.setup.models.species.model

    assert species_mdl.option() == "off"
    species_mdl.option = "species-transport"
    assert species_mdl.option() == "species-transport"

    # Test command names list
    materials = solver_session.setup.materials
    assert sorted(materials.mixture.command_names) == sorted(
        ["delete", "list", "list_properties", "make_a_copy", "rename"]
    )

    # Test change/creating a mixture with custom species from template
    custom_species_1 = materials.fluid.create("custom-species-1")
    custom_species_2 = materials.fluid.create("custom-species-2")
    solver_session.tui.define.materials.change_create(
        "mixture-template",  # Change/create mixture-template
        "custom-mixture",  # Rename to `custom-mixture`
        "yes",  # Change mixture species
        "2",  # Set number of species to 2
        custom_species_1.name(),  # Set species 1
        custom_species_2.name(),  # Set species 2
        "0",  # No surface species
        "0",  # No site species
        "no",  # Do not change density
        "no",  # Do not change specific heat
        "no",  # Do not change thermal conductivity
        "no",  # Do not change viscosity
        "no",  # Do not change mass diffusivity
        "no",  # Do not change speed of sound
        "yes",  # Overwrite mixture-template
    )
    assert "custom-mixture" in materials.mixture.keys()
    assert "mixture-template" not in materials.mixture.keys()

    # Test that mixture contains correct species
    mix_species = solver_session.setup.materials.mixture[
        "custom-mixture"
    ].species.volumetric_species.keys()
    assert "custom-species-1" in mix_species
    assert "custom-species-2" in mix_species

    # Test copying a mixture
    materials.mixture.make_a_copy(
        from_="custom-mixture",
        to="custom-mixture-copy",
    )
    assert "custom-mixture-copy" in materials.mixture.keys()

    # Test changing cellzone mixture
    elbow_zone = solver_session.setup.cell_zone_conditions.fluid["elbow-fluid"]
    assert elbow_zone.material() == "custom-mixture"
    elbow_zone.material = "custom-mixture-copy"
    assert elbow_zone.material() == "custom-mixture-copy"

    # Test deleting a mixture
    materials.mixture.delete(name_list=["custom-mixture"])
    assert "custom-mixture" not in materials.mixture.keys()
