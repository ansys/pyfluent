#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .coarsening_parameters_2 import coarsening_parameters
from .fixed_cycle_parameters_2 import fixed_cycle_parameters
from .options_1 import options
from .relaxation_factor import relaxation_factor


class fas_mg_controls(Group):
    """'fas_mg_controls' child."""

    fluent_name = "fas-mg-controls"

    child_names = [
        "fixed_cycle_parameters",
        "coarsening_parameters",
        "relaxation_factor",
        "options",
    ]

    fixed_cycle_parameters: fixed_cycle_parameters = fixed_cycle_parameters
    """
    fixed_cycle_parameters child of fas_mg_controls
    """
    coarsening_parameters: coarsening_parameters = coarsening_parameters
    """
    coarsening_parameters child of fas_mg_controls
    """
    relaxation_factor: relaxation_factor = relaxation_factor
    """
    relaxation_factor child of fas_mg_controls
    """
    options: options = options
    """
    options child of fas_mg_controls
    """
