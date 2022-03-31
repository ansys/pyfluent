#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .pressure_far_field_child import pressure_far_field_child


class pressure_far_field(NamedObject[pressure_far_field_child]):
    """'pressure_far_field' child."""

    fluent_name = "pressure-far-field"

    command_names = ["change_type"]

    change_type: change_type = change_type
    """
    change_type command of pressure_far_field
    """
    child_object_type: pressure_far_field_child = pressure_far_field_child
    """
    child_object_type of pressure_far_field.
    """
