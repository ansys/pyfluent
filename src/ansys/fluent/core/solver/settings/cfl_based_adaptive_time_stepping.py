#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enalbled import enalbled
from .user_defined_timestep import user_defined_timestep
from .desired_cfl import desired_cfl
from .time_end import time_end
from .initial_time_step import initial_time_step
from .max_fixed_time_step import max_fixed_time_step
from .update_interval_time_step_size import update_interval_time_step_size
from .min_time_step import min_time_step
from .max_time_step import max_time_step
from .min_step_change_factor import min_step_change_factor
from .max_step_change_factor import max_step_change_factor
class cfl_based_adaptive_time_stepping(Group):
    """
    'cfl_based_adaptive_time_stepping' child.
    """

    fluent_name = "cfl-based-adaptive-time-stepping"

    child_names = \
        ['enalbled', 'user_defined_timestep', 'desired_cfl', 'time_end',
         'initial_time_step', 'max_fixed_time_step',
         'update_interval_time_step_size', 'min_time_step', 'max_time_step',
         'min_step_change_factor', 'max_step_change_factor']

    enalbled: enalbled = enalbled
    """
    enalbled child of cfl_based_adaptive_time_stepping
    """
    user_defined_timestep: user_defined_timestep = user_defined_timestep
    """
    user_defined_timestep child of cfl_based_adaptive_time_stepping
    """
    desired_cfl: desired_cfl = desired_cfl
    """
    desired_cfl child of cfl_based_adaptive_time_stepping
    """
    time_end: time_end = time_end
    """
    time_end child of cfl_based_adaptive_time_stepping
    """
    initial_time_step: initial_time_step = initial_time_step
    """
    initial_time_step child of cfl_based_adaptive_time_stepping
    """
    max_fixed_time_step: max_fixed_time_step = max_fixed_time_step
    """
    max_fixed_time_step child of cfl_based_adaptive_time_stepping
    """
    update_interval_time_step_size: update_interval_time_step_size = update_interval_time_step_size
    """
    update_interval_time_step_size child of cfl_based_adaptive_time_stepping
    """
    min_time_step: min_time_step = min_time_step
    """
    min_time_step child of cfl_based_adaptive_time_stepping
    """
    max_time_step: max_time_step = max_time_step
    """
    max_time_step child of cfl_based_adaptive_time_stepping
    """
    min_step_change_factor: min_step_change_factor = min_step_change_factor
    """
    min_step_change_factor child of cfl_based_adaptive_time_stepping
    """
    max_step_change_factor: max_step_change_factor = max_step_change_factor
    """
    max_step_change_factor child of cfl_based_adaptive_time_stepping
    """
