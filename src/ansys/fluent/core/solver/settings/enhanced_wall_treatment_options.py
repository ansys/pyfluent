#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .pressure_gradient_effects import pressure_gradient_effects
from .thermal_effects import thermal_effects


class enhanced_wall_treatment_options(Group):
    """'enhanced_wall_treatment_options' child."""

    fluent_name = "enhanced-wall-treatment-options"

    child_names = ["pressure_gradient_effects", "thermal_effects"]

    pressure_gradient_effects: pressure_gradient_effects = (
        pressure_gradient_effects
    )
    """
    pressure_gradient_effects child of enhanced_wall_treatment_options
    """
    thermal_effects: thermal_effects = thermal_effects
    """
    thermal_effects child of enhanced_wall_treatment_options
    """
