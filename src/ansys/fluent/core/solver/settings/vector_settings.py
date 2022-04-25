#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant_color import constant_color
from .length_to_head_ratio import length_to_head_ratio
from .scale_1 import scale
from .style import style
from .vector_length import vector_length
from .vector_of import vector_of


class vector_settings(Group):
    """'vector_settings' child."""

    fluent_name = "vector-settings"

    child_names = [
        "style",
        "vector_length",
        "constant_color",
        "vector_of",
        "scale",
        "length_to_head_ratio",
    ]

    style: style = style
    """
    style child of vector_settings
    """
    vector_length: vector_length = vector_length
    """
    vector_length child of vector_settings
    """
    constant_color: constant_color = constant_color
    """
    constant_color child of vector_settings
    """
    vector_of: vector_of = vector_of
    """
    vector_of child of vector_settings
    """
    scale: scale = scale
    """
    scale child of vector_settings
    """
    length_to_head_ratio: length_to_head_ratio = length_to_head_ratio
    """
    length_to_head_ratio child of vector_settings
    """
