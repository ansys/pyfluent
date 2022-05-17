#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .custom_vector import custom_vector
from .field import field
from .surfaces import surfaces
from .geometry_1 import geometry
from .physics import physics
from .retain_instantaneous_values import retain_instantaneous_values
from .report_type import report_type
from .phase_25 import phase
from .average_over import average_over
from .per_surface import per_surface
from .old_props import old_props
from .surface_names import surface_names
from .surface_ids import surface_ids
class surface_child(Group):
    """
    'child_object_type' of surface
    """

    fluent_name = "child-object-type"

    child_names = \
        ['custom_vector', 'field', 'surfaces', 'geometry', 'physics',
         'retain_instantaneous_values', 'report_type', 'phase',
         'average_over', 'per_surface', 'old_props', 'surface_names',
         'surface_ids']

    custom_vector: custom_vector = custom_vector
    """
    custom_vector child of surface_child
    """
    field: field = field
    """
    field child of surface_child
    """
    surfaces: surfaces = surfaces
    """
    surfaces child of surface_child
    """
    geometry: geometry = geometry
    """
    geometry child of surface_child
    """
    physics: physics = physics
    """
    physics child of surface_child
    """
    retain_instantaneous_values: retain_instantaneous_values = retain_instantaneous_values
    """
    retain_instantaneous_values child of surface_child
    """
    report_type: report_type = report_type
    """
    report_type child of surface_child
    """
    phase: phase = phase
    """
    phase child of surface_child
    """
    average_over: average_over = average_over
    """
    average_over child of surface_child
    """
    per_surface: per_surface = per_surface
    """
    per_surface child of surface_child
    """
    old_props: old_props = old_props
    """
    old_props child of surface_child
    """
    surface_names: surface_names = surface_names
    """
    surface_names child of surface_child
    """
    surface_ids: surface_ids = surface_ids
    """
    surface_ids child of surface_child
    """
