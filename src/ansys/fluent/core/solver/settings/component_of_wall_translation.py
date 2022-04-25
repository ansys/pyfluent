#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .axis_direction_component_child import axis_direction_component_child


class component_of_wall_translation(
    ListObject[axis_direction_component_child]
):
    """'component_of_wall_translation' child."""

    fluent_name = "component-of-wall-translation"

    child_object_type: axis_direction_component_child = (
        axis_direction_component_child
    )
    """
    child_object_type of component_of_wall_translation.
    """
