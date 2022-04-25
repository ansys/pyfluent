#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .coupled_parameters import coupled_parameters
from .flexible_cycle_paramters import flexible_cycle_paramters
from .options_1 import options
from .scalar_parameters import scalar_parameters


class algebric_mg_controls(Group):
    """'algebric_mg_controls' child."""

    fluent_name = "algebric-mg-controls"

    child_names = [
        "scalar_parameters",
        "coupled_parameters",
        "flexible_cycle_paramters",
        "options",
    ]

    scalar_parameters: scalar_parameters = scalar_parameters
    """
    scalar_parameters child of algebric_mg_controls
    """
    coupled_parameters: coupled_parameters = coupled_parameters
    """
    coupled_parameters child of algebric_mg_controls
    """
    flexible_cycle_paramters: flexible_cycle_paramters = (
        flexible_cycle_paramters
    )
    """
    flexible_cycle_paramters child of algebric_mg_controls
    """
    options: options = options
    """
    options child of algebric_mg_controls
    """
