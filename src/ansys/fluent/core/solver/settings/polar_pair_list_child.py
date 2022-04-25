#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .polar_real_angle import polar_real_angle
from .polar_real_intensity import polar_real_intensity


class polar_pair_list_child(Group):
    """'child_object_type' of polar_pair_list."""

    fluent_name = "child-object-type"

    child_names = ["polar_real_angle", "polar_real_intensity"]

    polar_real_angle: polar_real_angle = polar_real_angle
    """
    polar_real_angle child of polar_pair_list_child
    """
    polar_real_intensity: polar_real_intensity = polar_real_intensity
    """
    polar_real_intensity child of polar_pair_list_child
    """
