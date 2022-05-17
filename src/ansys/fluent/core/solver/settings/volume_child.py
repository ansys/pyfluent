#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .geometry_1 import geometry
from .physics import physics
from .field import field
from .retain_instantaneous_values import retain_instantaneous_values
from .report_type import report_type
from .phase_25 import phase
from .average_over import average_over
from .per_zone import per_zone
from .old_props import old_props
from .zone_names import zone_names
from .expr_list import expr_list
from .zone_list import zone_list
class volume_child(Group):
    """
    'child_object_type' of volume
    """

    fluent_name = "child-object-type"

    child_names = \
        ['geometry', 'physics', 'field', 'retain_instantaneous_values',
         'report_type', 'phase', 'average_over', 'per_zone', 'old_props',
         'zone_names', 'expr_list', 'zone_list']

    geometry: geometry = geometry
    """
    geometry child of volume_child
    """
    physics: physics = physics
    """
    physics child of volume_child
    """
    field: field = field
    """
    field child of volume_child
    """
    retain_instantaneous_values: retain_instantaneous_values = retain_instantaneous_values
    """
    retain_instantaneous_values child of volume_child
    """
    report_type: report_type = report_type
    """
    report_type child of volume_child
    """
    phase: phase = phase
    """
    phase child of volume_child
    """
    average_over: average_over = average_over
    """
    average_over child of volume_child
    """
    per_zone: per_zone = per_zone
    """
    per_zone child of volume_child
    """
    old_props: old_props = old_props
    """
    old_props child of volume_child
    """
    zone_names: zone_names = zone_names
    """
    zone_names child of volume_child
    """
    expr_list: expr_list = expr_list
    """
    expr_list child of volume_child
    """
    zone_list: zone_list = zone_list
    """
    zone_list child of volume_child
    """
