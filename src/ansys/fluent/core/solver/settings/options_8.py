#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant_1 import constant
from .option import option
from .variable import variable


class options(Group):
    """'options' child."""

    fluent_name = "options"

    child_names = ["option", "constant", "variable"]

    option: option = option
    """
    option child of options
    """
    constant: constant = constant
    """
    constant child of options
    """
    variable: variable = variable
    """
    variable child of options
    """
