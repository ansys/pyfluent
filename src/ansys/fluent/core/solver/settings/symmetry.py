#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .axis_child import axis_child
from .change_type import change_type


class symmetry(NamedObject[axis_child]):
    """'symmetry' child."""

    fluent_name = "symmetry"

    command_names = ["change_type"]

    change_type: change_type = change_type
    """
    change_type command of symmetry
    """
    child_object_type: axis_child = axis_child
    """
    child_object_type of symmetry.
    """
