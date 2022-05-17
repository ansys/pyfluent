#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .wall_child import wall_child

class wall(NamedObject[wall_child]):
    """
    'wall' child.
    """

    fluent_name = "wall"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of wall
    """
    child_object_type: wall_child = wall_child
    """
    child_object_type of wall.
    """
