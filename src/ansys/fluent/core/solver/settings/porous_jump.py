#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .porous_jump_child import porous_jump_child


class porous_jump(NamedObject[porous_jump_child]):
    """'porous_jump' child."""

    fluent_name = "porous-jump"

    command_names = ["change_type"]

    change_type: change_type = change_type
    """
    change_type command of porous_jump
    """
    child_object_type: porous_jump_child = porous_jump_child
    """
    child_object_type of porous_jump.
    """
