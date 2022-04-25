#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .fluid_1 import fluid
from .solid_1 import solid


class cell_zone_conditions(Group):
    """'cell_zone_conditions' child."""

    fluent_name = "cell-zone-conditions"

    child_names = ["fluid", "solid"]

    fluid: fluid = fluid
    """
    fluid child of cell_zone_conditions
    """
    solid: solid = solid
    """
    solid child of cell_zone_conditions
    """
