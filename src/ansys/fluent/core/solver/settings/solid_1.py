#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .solid_child import solid_child


class solid(NamedObject[solid_child]):
    """'solid' child."""

    fluent_name = "solid"

    command_names = ["change_type"]

    change_type: change_type = change_type
    """
    change_type command of solid
    """
    child_object_type: solid_child = solid_child
    """
    child_object_type of solid.
    """
