#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .display_clipped_pressure import display_clipped_pressure
from .max_vapor_pressure_ratio import max_vapor_pressure_ratio
from .min_vapor_pressure import min_vapor_pressure
from .old_treatment_for_turbulent_diffusion import (
    old_treatment_for_turbulent_diffusion,
)
from .schnerr_cond_coeff import schnerr_cond_coeff
from .schnerr_evap_coeff import schnerr_evap_coeff
from .turbulent_diffusion import turbulent_diffusion


class cavitation(Group):
    """'cavitation' child."""

    fluent_name = "cavitation"

    child_names = [
        "schnerr_evap_coeff",
        "schnerr_cond_coeff",
        "max_vapor_pressure_ratio",
        "min_vapor_pressure",
        "display_clipped_pressure",
        "turbulent_diffusion",
        "old_treatment_for_turbulent_diffusion",
    ]

    schnerr_evap_coeff: schnerr_evap_coeff = schnerr_evap_coeff
    """
    schnerr_evap_coeff child of cavitation
    """
    schnerr_cond_coeff: schnerr_cond_coeff = schnerr_cond_coeff
    """
    schnerr_cond_coeff child of cavitation
    """
    max_vapor_pressure_ratio: max_vapor_pressure_ratio = (
        max_vapor_pressure_ratio
    )
    """
    max_vapor_pressure_ratio child of cavitation
    """
    min_vapor_pressure: min_vapor_pressure = min_vapor_pressure
    """
    min_vapor_pressure child of cavitation
    """
    display_clipped_pressure: display_clipped_pressure = (
        display_clipped_pressure
    )
    """
    display_clipped_pressure child of cavitation
    """
    turbulent_diffusion: turbulent_diffusion = turbulent_diffusion
    """
    turbulent_diffusion child of cavitation
    """
    old_treatment_for_turbulent_diffusion: old_treatment_for_turbulent_diffusion = (
        old_treatment_for_turbulent_diffusion
    )
    """
    old_treatment_for_turbulent_diffusion child of cavitation
    """
