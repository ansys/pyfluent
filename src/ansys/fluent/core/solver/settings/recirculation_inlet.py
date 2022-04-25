#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .recirculation_inlet_child import recirculation_inlet_child


class recirculation_inlet(NamedObject[recirculation_inlet_child]):
    """'recirculation_inlet' child."""

    fluent_name = "recirculation-inlet"

    command_names = ["change_type"]

    change_type: change_type = change_type
    """
    change_type command of recirculation_inlet
    """
    child_object_type: recirculation_inlet_child = recirculation_inlet_child
    """
    child_object_type of recirculation_inlet.
    """
