#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

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
class force_child(Group):
    """
    'child_object_type' of force
    """

    fluent_name = "child-object-type"

    child_names = \
        ['retain_instantaneous_values', 'scaled', 'report_type',
         'average_over', 'per_zone', 'thread_names', 'thread_ids',
         'old_props', 'reference_frame', 'force_vector']

    retain_instantaneous_values: retain_instantaneous_values = retain_instantaneous_values
    """
    retain_instantaneous_values child of force_child
    """
    scaled: scaled = scaled
    """
    scaled child of force_child
    """
    report_type: report_type = report_type
    """
    report_type child of force_child
    """
    average_over: average_over = average_over
    """
    average_over child of force_child
    """
    per_zone: per_zone = per_zone
    """
    per_zone child of force_child
    """
    thread_names: thread_names = thread_names
    """
    thread_names child of force_child
    """
    thread_ids: thread_ids = thread_ids
    """
    thread_ids child of force_child
    """
    old_props: old_props = old_props
    """
    old_props child of force_child
    """
    reference_frame: reference_frame = reference_frame
    """
    reference_frame child of force_child
    """
    force_vector: force_vector = force_vector
    """
    force_vector child of force_child
    """
