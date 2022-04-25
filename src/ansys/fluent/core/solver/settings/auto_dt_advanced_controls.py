#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .dt_factor_max import dt_factor_max
from .dt_factor_min import dt_factor_min
from .dt_init_limit import dt_init_limit
from .dt_max import dt_max
from .enable_1 import enable
from .max_velocity_ratio import max_velocity_ratio


class auto_dt_advanced_controls(Group):
    """'auto_dt_advanced_controls' child."""

    fluent_name = "auto-dt-advanced-controls"

    child_names = [
        "enable",
        "dt_init_limit",
        "dt_max",
        "dt_factor_min",
        "dt_factor_max",
        "max_velocity_ratio",
    ]

    enable: enable = enable
    """
    enable child of auto_dt_advanced_controls
    """
    dt_init_limit: dt_init_limit = dt_init_limit
    """
    dt_init_limit child of auto_dt_advanced_controls
    """
    dt_max: dt_max = dt_max
    """
    dt_max child of auto_dt_advanced_controls
    """
    dt_factor_min: dt_factor_min = dt_factor_min
    """
    dt_factor_min child of auto_dt_advanced_controls
    """
    dt_factor_max: dt_factor_max = dt_factor_max
    """
    dt_factor_max child of auto_dt_advanced_controls
    """
    max_velocity_ratio: max_velocity_ratio = max_velocity_ratio
    """
    max_velocity_ratio child of auto_dt_advanced_controls
    """
