#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .coarsen_by_interval_2 import coarsen_by_interval
from .max_coarse_levels_2 import max_coarse_levels


class coarsening_parameters(Group):
    """'coarsening_parameters' child."""

    fluent_name = "coarsening-parameters"

    child_names = ["max_coarse_levels", "coarsen_by_interval"]

    max_coarse_levels: max_coarse_levels = max_coarse_levels
    """
    max_coarse_levels child of coarsening_parameters
    """
    coarsen_by_interval: coarsen_by_interval = coarsen_by_interval
    """
    coarsen_by_interval child of coarsening_parameters
    """
