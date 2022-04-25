#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enabled_1 import enabled
from .turbulent_intensity import turbulent_intensity
from .turbulent_viscosity_ratio import turbulent_viscosity_ratio


class localized_turb_init(Group):
    """'localized_turb_init' child."""

    fluent_name = "localized-turb-init"

    child_names = [
        "enabled",
        "turbulent_intensity",
        "turbulent_viscosity_ratio",
    ]

    enabled: enabled = enabled
    """
    enabled child of localized_turb_init
    """
    turbulent_intensity: turbulent_intensity = turbulent_intensity
    """
    turbulent_intensity child of localized_turb_init
    """
    turbulent_viscosity_ratio: turbulent_viscosity_ratio = (
        turbulent_viscosity_ratio
    )
    """
    turbulent_viscosity_ratio child of localized_turb_init
    """
