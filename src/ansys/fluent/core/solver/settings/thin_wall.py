#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .shell_conduction_child import shell_conduction_child


class thin_wall(ListObject[shell_conduction_child]):
    """'thin_wall' child."""

    fluent_name = "thin-wall"

    child_object_type: shell_conduction_child = shell_conduction_child
    """
    child_object_type of thin_wall.
    """
