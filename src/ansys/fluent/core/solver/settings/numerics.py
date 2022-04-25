#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .alternate_diffusion_for_porous_region_solids import (
    alternate_diffusion_for_porous_region_solids,
)
from .disable_rhie_chow_flux import disable_rhie_chow_flux
from .first_to_second_order_blending_1 import first_to_second_order_blending
from .implicit_bodyforce_treatment import implicit_bodyforce_treatment
from .physical_velocity_formulation import physical_velocity_formulation
from .presto_pressure_scheme import presto_pressure_scheme
from .velocity_formulation import velocity_formulation


class numerics(Group):
    """'numerics' child."""

    fluent_name = "numerics"

    child_names = [
        "implicit_bodyforce_treatment",
        "velocity_formulation",
        "physical_velocity_formulation",
        "disable_rhie_chow_flux",
        "presto_pressure_scheme",
        "first_to_second_order_blending",
        "alternate_diffusion_for_porous_region_solids",
    ]

    implicit_bodyforce_treatment: implicit_bodyforce_treatment = (
        implicit_bodyforce_treatment
    )
    """
    implicit_bodyforce_treatment child of numerics
    """
    velocity_formulation: velocity_formulation = velocity_formulation
    """
    velocity_formulation child of numerics
    """
    physical_velocity_formulation: physical_velocity_formulation = (
        physical_velocity_formulation
    )
    """
    physical_velocity_formulation child of numerics
    """
    disable_rhie_chow_flux: disable_rhie_chow_flux = disable_rhie_chow_flux
    """
    disable_rhie_chow_flux child of numerics
    """
    presto_pressure_scheme: presto_pressure_scheme = presto_pressure_scheme
    """
    presto_pressure_scheme child of numerics
    """
    first_to_second_order_blending: first_to_second_order_blending = (
        first_to_second_order_blending
    )
    """
    first_to_second_order_blending child of numerics
    """
    alternate_diffusion_for_porous_region_solids: alternate_diffusion_for_porous_region_solids = (
        alternate_diffusion_for_porous_region_solids
    )
    """
    alternate_diffusion_for_porous_region_solids child of numerics
    """
