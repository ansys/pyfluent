#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enabled_2 import enabled
from .error_tolerance import error_tolerance
from .fixed_time_steps import fixed_time_steps
from .max_step_change_factor import max_step_change_factor
from .max_time_step import max_time_step
from .min_step_change_factor import min_step_change_factor
from .min_time_step import min_time_step
from .time_end import time_end
from .user_defined_timestep import user_defined_timestep


class adaptive_time_stepping(Group):
    """'adaptive_time_stepping' child."""

    fluent_name = "adaptive-time-stepping"

    child_names = [
        "enabled",
        "user_defined_timestep",
        "error_tolerance",
        "time_end",
        "min_time_step",
        "max_time_step",
        "min_step_change_factor",
        "max_step_change_factor",
        "fixed_time_steps",
    ]

    enabled: enabled = enabled
    """
    enabled child of adaptive_time_stepping
    """
    user_defined_timestep: user_defined_timestep = user_defined_timestep
    """
    user_defined_timestep child of adaptive_time_stepping
    """
    error_tolerance: error_tolerance = error_tolerance
    """
    error_tolerance child of adaptive_time_stepping
    """
    time_end: time_end = time_end
    """
    time_end child of adaptive_time_stepping
    """
    min_time_step: min_time_step = min_time_step
    """
    min_time_step child of adaptive_time_stepping
    """
    max_time_step: max_time_step = max_time_step
    """
    max_time_step child of adaptive_time_stepping
    """
    min_step_change_factor: min_step_change_factor = min_step_change_factor
    """
    min_step_change_factor child of adaptive_time_stepping
    """
    max_step_change_factor: max_step_change_factor = max_step_change_factor
    """
    max_step_change_factor child of adaptive_time_stepping
    """
    fixed_time_steps: fixed_time_steps = fixed_time_steps
    """
    fixed_time_steps child of adaptive_time_stepping
    """
