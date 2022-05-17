#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .axis_child import axis_child

class geometry(NamedObject[axis_child]):
    """
    'geometry' child.
    """

    fluent_name = "geometry"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of geometry
    """
    child_object_type: axis_child = axis_child
    """
    child_object_type of geometry.
    """
