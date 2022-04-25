#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .auto_scale import auto_scale
from .scale_f import scale_f


class scale(Group):
    """'scale' child."""

    fluent_name = "scale"

    child_names = ["auto_scale", "scale_f"]

    auto_scale: auto_scale = auto_scale
    """
    auto_scale child of scale
    """
    scale_f: scale_f = scale_f
    """
    scale_f child of scale
    """
