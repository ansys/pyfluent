#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .average_over import average_over
from .geometry_1 import geometry
from .old_props import old_props
from .per_zone import per_zone
from .phase_25 import phase
from .physics import physics
from .report_type import report_type
from .retain_instantaneous_values import retain_instantaneous_values
from .zone_ids import zone_ids
from .zone_names import zone_names


class flux_child(Group):
    """'child_object_type' of flux."""

    fluent_name = "child-object-type"

    child_names = [
        "geometry",
        "physics",
        "retain_instantaneous_values",
        "report_type",
        "phase",
        "average_over",
        "per_zone",
        "old_props",
        "zone_names",
        "zone_ids",
    ]

    geometry: geometry = geometry
    """
    geometry child of flux_child
    """
    physics: physics = physics
    """
    physics child of flux_child
    """
    retain_instantaneous_values: retain_instantaneous_values = (
        retain_instantaneous_values
    )
    """
    retain_instantaneous_values child of flux_child
    """
    report_type: report_type = report_type
    """
    report_type child of flux_child
    """
    phase: phase = phase
    """
    phase child of flux_child
    """
    average_over: average_over = average_over
    """
    average_over child of flux_child
    """
    per_zone: per_zone = per_zone
    """
    per_zone child of flux_child
    """
    old_props: old_props = old_props
    """
    old_props child of flux_child
    """
    zone_names: zone_names = zone_names
    """
    zone_names child of flux_child
    """
    zone_ids: zone_ids = zone_ids
    """
    zone_ids child of flux_child
    """
