#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .geom_bgthread import geom_bgthread
from .geom_dir_spec import geom_dir_spec
from .geom_dir_x import geom_dir_x
from .geom_dir_y import geom_dir_y
from .geom_dir_z import geom_dir_z
from .geom_disable import geom_disable
from .geom_levels import geom_levels
from .non_overlap_zone_name import non_overlap_zone_name
from .phase_7 import phase


class interface_child(Group):
    """'child_object_type' of interface."""

    fluent_name = "child-object-type"

    child_names = [
        "phase",
        "geom_disable",
        "geom_dir_spec",
        "geom_dir_x",
        "geom_dir_y",
        "geom_dir_z",
        "geom_levels",
        "geom_bgthread",
        "non_overlap_zone_name",
    ]

    phase: phase = phase
    """
    phase child of interface_child
    """
    geom_disable: geom_disable = geom_disable
    """
    geom_disable child of interface_child
    """
    geom_dir_spec: geom_dir_spec = geom_dir_spec
    """
    geom_dir_spec child of interface_child
    """
    geom_dir_x: geom_dir_x = geom_dir_x
    """
    geom_dir_x child of interface_child
    """
    geom_dir_y: geom_dir_y = geom_dir_y
    """
    geom_dir_y child of interface_child
    """
    geom_dir_z: geom_dir_z = geom_dir_z
    """
    geom_dir_z child of interface_child
    """
    geom_levels: geom_levels = geom_levels
    """
    geom_levels child of interface_child
    """
    geom_bgthread: geom_bgthread = geom_bgthread
    """
    geom_bgthread child of interface_child
    """
    non_overlap_zone_name: non_overlap_zone_name = non_overlap_zone_name
    """
    non_overlap_zone_name child of interface_child
    """
