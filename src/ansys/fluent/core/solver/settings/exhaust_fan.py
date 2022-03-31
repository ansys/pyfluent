#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .exhaust_fan_child import exhaust_fan_child


class exhaust_fan(NamedObject[exhaust_fan_child]):
    """'exhaust_fan' child."""

    fluent_name = "exhaust-fan"

    command_names = ["change_type"]

    change_type: change_type = change_type
    """
    change_type command of exhaust_fan
    """
    child_object_type: exhaust_fan_child = exhaust_fan_child
    """
    child_object_type of exhaust_fan.
    """
