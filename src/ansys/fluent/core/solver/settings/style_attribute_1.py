#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .style import style
from .line_width import line_width
from .arrow_space import arrow_space
from .arrow_scale import arrow_scale
from .marker_size import marker_size
from .sphere_size import sphere_size
from .sphere_lod import sphere_lod
from .radius import radius
from .ribbon_settings import ribbon_settings
from .sphere_settings import sphere_settings
class style_attribute(Group):
    """
    'style_attribute' child.
    """

    fluent_name = "style-attribute"

    child_names = \
        ['style', 'line_width', 'arrow_space', 'arrow_scale', 'marker_size',
         'sphere_size', 'sphere_lod', 'radius', 'ribbon_settings',
         'sphere_settings']

    style: style = style
    """
    style child of style_attribute
    """
    line_width: line_width = line_width
    """
    line_width child of style_attribute
    """
    arrow_space: arrow_space = arrow_space
    """
    arrow_space child of style_attribute
    """
    arrow_scale: arrow_scale = arrow_scale
    """
    arrow_scale child of style_attribute
    """
    marker_size: marker_size = marker_size
    """
    marker_size child of style_attribute
    """
    sphere_size: sphere_size = sphere_size
    """
    sphere_size child of style_attribute
    """
    sphere_lod: sphere_lod = sphere_lod
    """
    sphere_lod child of style_attribute
    """
    radius: radius = radius
    """
    radius child of style_attribute
    """
    ribbon_settings: ribbon_settings = ribbon_settings
    """
    ribbon_settings child of style_attribute
    """
    sphere_settings: sphere_settings = sphere_settings
    """
    sphere_settings child of style_attribute
    """
