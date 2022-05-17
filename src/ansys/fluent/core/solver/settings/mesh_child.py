#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .zone_ids import zone_ids
from .retain_instantaneous_values import retain_instantaneous_values
from .old_props import old_props
from .zone_names import zone_names
from .zone_list import zone_list
from .average_over import average_over
from .per_zone import per_zone
class mesh_child(Group):
    """
    'child_object_type' of mesh
    """

    fluent_name = "child-object-type"

    child_names = \
        ['zone_ids', 'retain_instantaneous_values', 'old_props', 'zone_names',
         'zone_list', 'average_over', 'per_zone']

    zone_ids: zone_ids = zone_ids
    """
    zone_ids child of mesh_child
    """
    retain_instantaneous_values: retain_instantaneous_values = retain_instantaneous_values
    """
    retain_instantaneous_values child of mesh_child
    """
    old_props: old_props = old_props
    """
    old_props child of mesh_child
    """
    zone_names: zone_names = zone_names
    """
    zone_names child of mesh_child
    """
    zone_list: zone_list = zone_list
    """
    zone_list child of mesh_child
    """
    average_over: average_over = average_over
    """
    average_over child of mesh_child
    """
    per_zone: per_zone = per_zone
    """
    per_zone child of mesh_child
    """
