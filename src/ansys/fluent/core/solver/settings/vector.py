#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .display import display
from .vector_child import vector_child


class vector(NamedObject[vector_child]):
    """'vector' child."""

    fluent_name = "vector"

    command_names = ["display"]

    display: display = display
    """
    display command of vector
    """
    child_object_type: vector_child = vector_child
    """
    child_object_type of vector.
    """
