#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .node_values_1 import node_values


class options(Group):
    """'options' child."""

    fluent_name = "options"

    child_names = ["node_values"]

    node_values: node_values = node_values
    """
    node_values child of options
    """
