#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .x_axis_function import x_axis_function
from .enabled_2 import enabled
class plot(Group):
    """
    'plot' child.
    """

    fluent_name = "plot"

    child_names = \
        ['x_axis_function', 'enabled']

    x_axis_function: x_axis_function = x_axis_function
    """
    x_axis_function child of plot
    """
    enabled: enabled = enabled
    """
    enabled child of plot
    """
