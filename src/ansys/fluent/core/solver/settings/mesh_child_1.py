#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .coloring import coloring
from .display_1 import display
from .display_state_name import display_state_name
from .edge_type import edge_type
from .geometry_1 import geometry
from .name import name
from .options_4 import options
from .physics import physics
from .shrink_factor import shrink_factor
from .surfaces import surfaces
from .surfaces_list import surfaces_list


class mesh_child(Group):
    """'child_object_type' of mesh."""

    fluent_name = "child-object-type"

    child_names = [
        "name",
        "options",
        "edge_type",
        "shrink_factor",
        "surfaces_list",
        "coloring",
        "display_state_name",
        "physics",
        "geometry",
        "surfaces",
    ]

    name: name = name
    """
    name child of mesh_child
    """
    options: options = options
    """
    options child of mesh_child
    """
    edge_type: edge_type = edge_type
    """
    edge_type child of mesh_child
    """
    shrink_factor: shrink_factor = shrink_factor
    """
    shrink_factor child of mesh_child
    """
    surfaces_list: surfaces_list = surfaces_list
    """
    surfaces_list child of mesh_child
    """
    coloring: coloring = coloring
    """
    coloring child of mesh_child
    """
    display_state_name: display_state_name = display_state_name
    """
    display_state_name child of mesh_child
    """
    physics: physics = physics
    """
    physics child of mesh_child
    """
    geometry: geometry = geometry
    """
    geometry child of mesh_child
    """
    surfaces: surfaces = surfaces
    """
    surfaces child of mesh_child
    """
    command_names = ["display"]

    display: display = display
    """
    display command of mesh_child
    """
