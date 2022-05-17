#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .normalization import normalization
from .integrate_over import integrate_over
from .report_type import report_type
from .average_over import average_over
from .per_zone import per_zone
from .old_props import old_props
from .thread_names import thread_names
from .thread_ids import thread_ids
class aeromechanics_child(Group):
    """
    'child_object_type' of aeromechanics
    """

    fluent_name = "child-object-type"

    child_names = \
        ['normalization', 'integrate_over', 'report_type', 'average_over',
         'per_zone', 'old_props', 'thread_names', 'thread_ids']

    normalization: normalization = normalization
    """
    normalization child of aeromechanics_child
    """
    integrate_over: integrate_over = integrate_over
    """
    integrate_over child of aeromechanics_child
    """
    report_type: report_type = report_type
    """
    report_type child of aeromechanics_child
    """
    average_over: average_over = average_over
    """
    average_over child of aeromechanics_child
    """
    per_zone: per_zone = per_zone
    """
    per_zone child of aeromechanics_child
    """
    old_props: old_props = old_props
    """
    old_props child of aeromechanics_child
    """
    thread_names: thread_names = thread_names
    """
    thread_names child of aeromechanics_child
    """
    thread_ids: thread_ids = thread_ids
    """
    thread_ids child of aeromechanics_child
    """
