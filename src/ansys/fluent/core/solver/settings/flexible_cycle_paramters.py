#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .max_coarse_relaxations import max_coarse_relaxations
from .max_fine_relaxations import max_fine_relaxations


class flexible_cycle_paramters(Group):
    """'flexible_cycle_paramters' child."""

    fluent_name = "flexible-cycle-paramters"

    child_names = ["max_fine_relaxations", "max_coarse_relaxations"]

    max_fine_relaxations: max_fine_relaxations = max_fine_relaxations
    """
    max_fine_relaxations child of flexible_cycle_paramters
    """
    max_coarse_relaxations: max_coarse_relaxations = max_coarse_relaxations
    """
    max_coarse_relaxations child of flexible_cycle_paramters
    """
