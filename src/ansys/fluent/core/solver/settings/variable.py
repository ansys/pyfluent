#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .range import range
from .size_by import size_by


class variable(Group):
    """'variable' child."""

    fluent_name = "variable"

    child_names = ["size_by", "range"]

    size_by: size_by = size_by
    """
    size_by child of variable
    """
    range: range = range
    """
    range child of variable
    """
