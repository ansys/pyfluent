#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .global_range import global_range


class auto_range_on(Group):
    """'auto_range_on' child."""

    fluent_name = "auto-range-on"

    child_names = ["global_range"]

    global_range: global_range = global_range
    """
    global_range child of auto_range_on
    """
