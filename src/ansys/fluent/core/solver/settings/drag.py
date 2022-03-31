#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .lift_child import lift_child


class drag(NamedObject[lift_child]):
    """'drag' child."""

    fluent_name = "drag"

    child_object_type: lift_child = lift_child
    """
    child_object_type of drag.
    """
