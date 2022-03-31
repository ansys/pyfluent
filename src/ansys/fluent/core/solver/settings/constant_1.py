#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .diameter import diameter


class constant(Group):
    """'constant' child."""

    fluent_name = "constant"

    child_names = ["diameter"]

    diameter: diameter = diameter
    """
    diameter child of constant
    """
