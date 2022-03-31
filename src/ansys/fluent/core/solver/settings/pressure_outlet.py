#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .pressure_outlet_child import pressure_outlet_child


class pressure_outlet(NamedObject[pressure_outlet_child]):
    """'pressure_outlet' child."""

    fluent_name = "pressure-outlet"

    command_names = ["change_type"]

    change_type: change_type = change_type
    """
    change_type command of pressure_outlet
    """
    child_object_type: pressure_outlet_child = pressure_outlet_child
    """
    child_object_type of pressure_outlet.
    """
