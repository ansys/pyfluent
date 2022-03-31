#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .outflow_child import outflow_child


class outflow(NamedObject[outflow_child]):
    """'outflow' child."""

    fluent_name = "outflow"

    command_names = ["change_type"]

    change_type: change_type = change_type
    """
    change_type command of outflow
    """
    child_object_type: outflow_child = outflow_child
    """
    child_object_type of outflow.
    """
