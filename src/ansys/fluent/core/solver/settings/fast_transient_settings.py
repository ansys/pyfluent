#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .rk2 import rk2


class fast_transient_settings(Group):
    """'fast_transient_settings' child."""

    fluent_name = "fast-transient-settings"

    child_names = ["rk2"]

    rk2: rk2 = rk2
    """
    rk2 child of fast_transient_settings
    """
