#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .intake_fan_child import intake_fan_child


class intake_fan(NamedObject[intake_fan_child]):
    """'intake_fan' child."""

    fluent_name = "intake-fan"

    command_names = ["change_type"]

    change_type: change_type = change_type
    """
    change_type command of intake_fan
    """
    child_object_type: intake_fan_child = intake_fan_child
    """
    child_object_type of intake_fan.
    """
