#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enabled_2 import enabled
from .color import color
class constant_color(Group):
    """
    'constant_color' child.
    """

    fluent_name = "constant-color"

    child_names = \
        ['enabled', 'color']

    enabled: enabled = enabled
    """
    enabled child of constant_color
    """
    color: color = color
    """
    color child of constant_color
    """
