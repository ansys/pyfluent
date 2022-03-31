#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .vof_smooth_options import vof_smooth_options


class patch(Group):
    """'patch' child."""

    fluent_name = "patch"

    child_names = ["vof_smooth_options"]

    vof_smooth_options: vof_smooth_options = vof_smooth_options
    """
    vof_smooth_options child of patch
    """
