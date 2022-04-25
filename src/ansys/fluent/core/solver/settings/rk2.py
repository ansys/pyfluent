#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .default_multi_stage_runge_kutta import default_multi_stage_runge_kutta
from .two_stage_runge_kutta import two_stage_runge_kutta


class rk2(Group):
    """'rk2' child."""

    fluent_name = "rk2"

    child_names = ["two_stage_runge_kutta", "default_multi_stage_runge_kutta"]

    two_stage_runge_kutta: two_stage_runge_kutta = two_stage_runge_kutta
    """
    two_stage_runge_kutta child of rk2
    """
    default_multi_stage_runge_kutta: default_multi_stage_runge_kutta = (
        default_multi_stage_runge_kutta
    )
    """
    default_multi_stage_runge_kutta child of rk2
    """
