#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .anti_aliasing import anti_aliasing
from .axes import axes
from .boundary_marker import boundary_marker
from .dynamic_shadows import dynamic_shadows
from .front_faces_transparent import front_faces_transparent
from .grid_plane import grid_plane
from .headlights import headlights
from .lighting import lighting
from .projection_1 import projection
from .reflections import reflections
from .ruler import ruler
from .static_shadows import static_shadows
from .title import title
from .view_name import view_name


class display_states_child(Group):
    """'child_object_type' of display_states."""

    fluent_name = "child-object-type"

    child_names = [
        "front_faces_transparent",
        "projection",
        "axes",
        "ruler",
        "title",
        "boundary_marker",
        "anti_aliasing",
        "reflections",
        "static_shadows",
        "dynamic_shadows",
        "grid_plane",
        "headlights",
        "lighting",
        "view_name",
    ]

    front_faces_transparent: front_faces_transparent = front_faces_transparent
    """
    front_faces_transparent child of display_states_child
    """
    projection: projection = projection
    """
    projection child of display_states_child
    """
    axes: axes = axes
    """
    axes child of display_states_child
    """
    ruler: ruler = ruler
    """
    ruler child of display_states_child
    """
    title: title = title
    """
    title child of display_states_child
    """
    boundary_marker: boundary_marker = boundary_marker
    """
    boundary_marker child of display_states_child
    """
    anti_aliasing: anti_aliasing = anti_aliasing
    """
    anti_aliasing child of display_states_child
    """
    reflections: reflections = reflections
    """
    reflections child of display_states_child
    """
    static_shadows: static_shadows = static_shadows
    """
    static_shadows child of display_states_child
    """
    dynamic_shadows: dynamic_shadows = dynamic_shadows
    """
    dynamic_shadows child of display_states_child
    """
    grid_plane: grid_plane = grid_plane
    """
    grid_plane child of display_states_child
    """
    headlights: headlights = headlights
    """
    headlights child of display_states_child
    """
    lighting: lighting = lighting
    """
    lighting child of display_states_child
    """
    view_name: view_name = view_name
    """
    view_name child of display_states_child
    """
