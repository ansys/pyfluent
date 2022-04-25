#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .inlet_vent_child import inlet_vent_child


class inlet_vent(NamedObject[inlet_vent_child]):
    """'inlet_vent' child."""

    fluent_name = "inlet-vent"

    command_names = ["change_type"]

    change_type: change_type = change_type
    """
    change_type command of inlet_vent
    """
    child_object_type: inlet_vent_child = inlet_vent_child
    """
    child_object_type of inlet_vent.
    """
