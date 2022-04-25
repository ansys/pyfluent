#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .fluid_child import fluid_child


class solid(NamedObject[fluid_child]):
    """'solid' child."""

    fluent_name = "solid"

    child_object_type: fluid_child = fluid_child
    """
    child_object_type of solid.
    """
