import pytest


@pytest.mark.quick
@pytest.mark.setup
@pytest.mark.fluent_version("latest")
def test_species_material(load_mixing_elbow_mesh):
    solver_session = load_mixing_elbow_mesh

    # Test turning on species transport model
    species_mdl = solver_session.setup.models.species.model

    assert species_mdl.option.get_state() == "off"
    species_mdl.option = "species-transport"
    assert species_mdl.option.get_state() == "species-transport"

    # Create custom species
    materials = solver_session.setup.materials

    custom_species_1 = materials.fluid.create("custom-species-1")
    custom_species_2 = materials.fluid.create("custom-species-2")

    # Test change/creating a mixture from template
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

    # Test copying a mixture
    materials.mixture.make_a_copy(
        from_="custom-mixture",
        to="custom-mixture-copy",
    )
    assert "custom-mixture-copy" in materials.mixture.keys()

    # Test deleting a mixture
    solver_session.tui.define.materials.delete("custom-mixture-copy")
    assert "custom-mixture-copy" not in materials.mixture.keys()

    # Check command names list
    assert materials.mixture.command_names == [
        "delete",
        "list",
        "list_properties",
        "make_a_copy",
    ]
