#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .axis_child import axis_child

class degassing(NamedObject[axis_child]):
    """
    'degassing' child.
    """

    fluent_name = "degassing"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of degassing
    """
    child_object_type: axis_child = axis_child
    """
    child_object_type of degassing.
    """
