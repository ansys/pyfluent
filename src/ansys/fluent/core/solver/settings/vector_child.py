#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .color_map import color_map
from .display_1 import display
from .display_state_name import display_state_name
from .draw_mesh import draw_mesh
from .field import field
from .geometry_1 import geometry
from .mesh_object import mesh_object
from .name import name
from .physics import physics
from .range_option import range_option
from .scale import scale
from .skip import skip
from .style import style
from .surfaces import surfaces
from .surfaces_list import surfaces_list
from .vector_field import vector_field
from .vector_opt import vector_opt


class vector_child(Group):
    """'child_object_type' of vector."""

    fluent_name = "child-object-type"

    child_names = [
        "name",
        "field",
        "vector_field",
        "surfaces_list",
        "scale",
        "style",
        "skip",
        "vector_opt",
        "range_option",
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
    name child of vector_child
    """
    field: field = field
    """
    field child of vector_child
    """
    vector_field: vector_field = vector_field
    """
    vector_field child of vector_child
    """
    surfaces_list: surfaces_list = surfaces_list
    """
    surfaces_list child of vector_child
    """
    scale: scale = scale
    """
    scale child of vector_child
    """
    style: style = style
    """
    style child of vector_child
    """
    skip: skip = skip
    """
    skip child of vector_child
    """
    vector_opt: vector_opt = vector_opt
    """
    vector_opt child of vector_child
    """
    range_option: range_option = range_option
    """
    range_option child of vector_child
    """
    color_map: color_map = color_map
    """
    color_map child of vector_child
    """
    draw_mesh: draw_mesh = draw_mesh
    """
    draw_mesh child of vector_child
    """
    mesh_object: mesh_object = mesh_object
    """
    mesh_object child of vector_child
    """
    display_state_name: display_state_name = display_state_name
    """
    display_state_name child of vector_child
    """
    physics: physics = physics
    """
    physics child of vector_child
    """
    geometry: geometry = geometry
    """
    geometry child of vector_child
    """
    surfaces: surfaces = surfaces
    """
    surfaces child of vector_child
    """
    command_names = ["display"]

    display: display = display
    """
    display command of vector_child
    """
