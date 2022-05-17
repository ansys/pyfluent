#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .name import name
from .uid import uid
from .options_5 import options
from .range import range
from .style_attribute import style_attribute
from .accuracy_control import accuracy_control
from .plot import plot
from .step import step
from .skip import skip
from .coarsen import coarsen
from .onzone import onzone
from .field import field
from .surfaces_list import surfaces_list
from .velocity_domain import velocity_domain
from .color_map import color_map
from .draw_mesh import draw_mesh
from .mesh_object import mesh_object
from .display_state_name import display_state_name
from .physics import physics
from .geometry_1 import geometry
from .surfaces import surfaces
from .display_1 import display
class pathlines_child(Group):
    """
    'child_object_type' of pathlines
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'uid', 'options', 'range', 'style_attribute',
         'accuracy_control', 'plot', 'step', 'skip', 'coarsen', 'onzone',
         'field', 'surfaces_list', 'velocity_domain', 'color_map',
         'draw_mesh', 'mesh_object', 'display_state_name', 'physics',
         'geometry', 'surfaces']

    name: name = name
    """
    name child of pathlines_child
    """
    uid: uid = uid
    """
    uid child of pathlines_child
    """
    options: options = options
    """
    options child of pathlines_child
    """
    range: range = range
    """
    range child of pathlines_child
    """
    style_attribute: style_attribute = style_attribute
    """
    style_attribute child of pathlines_child
    """
    accuracy_control: accuracy_control = accuracy_control
    """
    accuracy_control child of pathlines_child
    """
    plot: plot = plot
    """
    plot child of pathlines_child
    """
    step: step = step
    """
    step child of pathlines_child
    """
    skip: skip = skip
    """
    skip child of pathlines_child
    """
    coarsen: coarsen = coarsen
    """
    coarsen child of pathlines_child
    """
    onzone: onzone = onzone
    """
    onzone child of pathlines_child
    """
    field: field = field
    """
    field child of pathlines_child
    """
    surfaces_list: surfaces_list = surfaces_list
    """
    surfaces_list child of pathlines_child
    """
    velocity_domain: velocity_domain = velocity_domain
    """
    velocity_domain child of pathlines_child
    """
    color_map: color_map = color_map
    """
    color_map child of pathlines_child
    """
    draw_mesh: draw_mesh = draw_mesh
    """
    draw_mesh child of pathlines_child
    """
    mesh_object: mesh_object = mesh_object
    """
    mesh_object child of pathlines_child
    """
    display_state_name: display_state_name = display_state_name
    """
    display_state_name child of pathlines_child
    """
    physics: physics = physics
    """
    physics child of pathlines_child
    """
    geometry: geometry = geometry
    """
    geometry child of pathlines_child
    """
    surfaces: surfaces = surfaces
    """
    surfaces child of pathlines_child
    """
    command_names = \
        ['display']

    display: display = display
    """
    display command of pathlines_child
    """
