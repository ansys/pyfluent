#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .coarsening_parameters import coarsening_parameters
from .fixed_cycle_parameters import fixed_cycle_parameters
from .smoother_type import smoother_type


class scalar_parameters(Group):
    """'scalar_parameters' child."""

    fluent_name = "scalar-parameters"

    child_names = [
        "fixed_cycle_parameters",
        "coarsening_parameters",
        "smoother_type",
    ]

    fixed_cycle_parameters: fixed_cycle_parameters = fixed_cycle_parameters
    """
    fixed_cycle_parameters child of scalar_parameters
    """
    coarsening_parameters: coarsening_parameters = coarsening_parameters
    """
    coarsening_parameters child of scalar_parameters
    """
    smoother_type: smoother_type = smoother_type
    """
    smoother_type child of scalar_parameters
    """
