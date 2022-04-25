#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .color import color
from .fixed_length import fixed_length
from .in_plane import in_plane
from .scale_head import scale_head
from .x_comp import x_comp
from .y_comp import y_comp
from .z_comp import z_comp


class vector_opt(Group):
    """'vector_opt' child."""

    fluent_name = "vector-opt"

    child_names = [
        "in_plane",
        "fixed_length",
        "x_comp",
        "y_comp",
        "z_comp",
        "scale_head",
        "color",
    ]

    in_plane: in_plane = in_plane
    """
    in_plane child of vector_opt
    """
    fixed_length: fixed_length = fixed_length
    """
    fixed_length child of vector_opt
    """
    x_comp: x_comp = x_comp
    """
    x_comp child of vector_opt
    """
    y_comp: y_comp = y_comp
    """
    y_comp child of vector_opt
    """
    z_comp: z_comp = z_comp
    """
    z_comp child of vector_opt
    """
    scale_head: scale_head = scale_head
    """
    scale_head child of vector_opt
    """
    color: color = color
    """
    color child of vector_opt
    """
