#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .heat_flux_relaxation_factor import heat_flux_relaxation_factor
from .show_expert_options import show_expert_options
from .two_resistance_boiling_framework import two_resistance_boiling_framework


class boiling(Group):
    """'boiling' child."""

    fluent_name = "boiling"

    child_names = [
        "heat_flux_relaxation_factor",
        "show_expert_options",
        "two_resistance_boiling_framework",
    ]

    heat_flux_relaxation_factor: heat_flux_relaxation_factor = (
        heat_flux_relaxation_factor
    )
    """
    heat_flux_relaxation_factor child of boiling
    """
    show_expert_options: show_expert_options = show_expert_options
    """
    show_expert_options child of boiling
    """
    two_resistance_boiling_framework: two_resistance_boiling_framework = (
        two_resistance_boiling_framework
    )
    """
    two_resistance_boiling_framework child of boiling
    """
