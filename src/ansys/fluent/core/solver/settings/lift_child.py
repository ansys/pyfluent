#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .geometry_1 import geometry
from .physics import physics
from .retain_instantaneous_values import retain_instantaneous_values
from .scaled import scaled
from .report_type import report_type
from .average_over import average_over
from .per_zone import per_zone
from .thread_names import thread_names
from .thread_ids import thread_ids
from .old_props import old_props
from .reference_frame import reference_frame
from .force_vector import force_vector
class lift_child(Group):
    """
    'child_object_type' of lift
    """

    fluent_name = "child-object-type"

    child_names = \
        ['geometry', 'physics', 'retain_instantaneous_values', 'scaled',
         'report_type', 'average_over', 'per_zone', 'thread_names',
         'thread_ids', 'old_props', 'reference_frame', 'force_vector']

    geometry: geometry = geometry
    """
    geometry child of lift_child
    """
    physics: physics = physics
    """
    physics child of lift_child
    """
    retain_instantaneous_values: retain_instantaneous_values = retain_instantaneous_values
    """
    retain_instantaneous_values child of lift_child
    """
    scaled: scaled = scaled
    """
    scaled child of lift_child
    """
    report_type: report_type = report_type
    """
    report_type child of lift_child
    """
    average_over: average_over = average_over
    """
    average_over child of lift_child
    """
    per_zone: per_zone = per_zone
    """
    per_zone child of lift_child
    """
    thread_names: thread_names = thread_names
    """
    thread_names child of lift_child
    """
    thread_ids: thread_ids = thread_ids
    """
    thread_ids child of lift_child
    """
    old_props: old_props = old_props
    """
    old_props child of lift_child
    """
    reference_frame: reference_frame = reference_frame
    """
    reference_frame child of lift_child
    """
    force_vector: force_vector = force_vector
    """
    force_vector child of lift_child
    """
