#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant_length import constant_length
from .option import option
from .variable_length import variable_length


class vector_length(Group):
    """'vector_length' child."""

    fluent_name = "vector-length"

    child_names = ["option", "constant_length", "variable_length"]

    option: option = option
    """
    option child of vector_length
    """
    constant_length: constant_length = constant_length
    """
    constant_length child of vector_length
    """
    variable_length: variable_length = variable_length
    """
    variable_length child of vector_length
    """
