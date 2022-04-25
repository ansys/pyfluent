#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .boundary_values import boundary_values
from .color_map import color_map
from .coloring_1 import coloring
from .contour_lines import contour_lines
from .display_1 import display
from .display_state_name import display_state_name
from .draw_mesh import draw_mesh
from .field import field
from .filled import filled
from .geometry_1 import geometry
from .mesh_object import mesh_object
from .name import name
from .node_values import node_values
from .physics import physics
from .range_option import range_option
from .surfaces import surfaces
from .surfaces_list import surfaces_list


class contour_child(Group):
    """'child_object_type' of contour."""

    fluent_name = "child-object-type"

    child_names = [
        "name",
        "field",
        "filled",
        "boundary_values",
        "contour_lines",
        "node_values",
        "surfaces_list",
        "range_option",
        "coloring",
        "color_map",
        "draw_mesh",
        "mesh_object",
        "display_state_name",
        "physics",
        "geometry",
        "surfaces",
    ]

    name: name = name
    """
    name child of contour_child
    """
    field: field = field
    """
    field child of contour_child
    """
    filled: filled = filled
    """
    filled child of contour_child
    """
    boundary_values: boundary_values = boundary_values
    """
    boundary_values child of contour_child
    """
    contour_lines: contour_lines = contour_lines
    """
    contour_lines child of contour_child
    """
    node_values: node_values = node_values
    """
    node_values child of contour_child
    """
    surfaces_list: surfaces_list = surfaces_list
    """
    surfaces_list child of contour_child
    """
    range_option: range_option = range_option
    """
    range_option child of contour_child
    """
    coloring: coloring = coloring
    """
    coloring child of contour_child
    """
    color_map: color_map = color_map
    """
    color_map child of contour_child
    """
    draw_mesh: draw_mesh = draw_mesh
    """
    draw_mesh child of contour_child
    """
    mesh_object: mesh_object = mesh_object
    """
    mesh_object child of contour_child
    """
    display_state_name: display_state_name = display_state_name
    """
    display_state_name child of contour_child
    """
    physics: physics = physics
    """
    physics child of contour_child
    """
    geometry: geometry = geometry
    """
    geometry child of contour_child
    """
    surfaces: surfaces = surfaces
    """
    surfaces child of contour_child
    """
    command_names = ["display"]

    display: display = display
    """
    display command of contour_child
    """
