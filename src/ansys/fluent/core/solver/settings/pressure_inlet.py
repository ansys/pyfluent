#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .pressure_inlet_child import pressure_inlet_child

class pressure_inlet(NamedObject[pressure_inlet_child]):
    """
    'pressure_inlet' child.
    """

    fluent_name = "pressure-inlet"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of pressure_inlet
    """
    child_object_type: pressure_inlet_child = pressure_inlet_child
    """
    child_object_type of pressure_inlet.
    """
