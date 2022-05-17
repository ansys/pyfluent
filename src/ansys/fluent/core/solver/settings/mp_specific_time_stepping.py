#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enabled_2 import enabled
from .global_courant_number import global_courant_number
from .initial_time_step_size import initial_time_step_size
from .fixed_time_step_size import fixed_time_step_size
from .min_time_step_size import min_time_step_size
from .max_time_step_size import max_time_step_size
from .min_step_change_factor import min_step_change_factor
from .max_step_change_factor import max_step_change_factor
from .update_interval import update_interval
class mp_specific_time_stepping(Group):
    """
    'mp_specific_time_stepping' child.
    """

    fluent_name = "mp-specific-time-stepping"

    child_names = \
        ['enabled', 'global_courant_number', 'initial_time_step_size',
         'fixed_time_step_size', 'min_time_step_size', 'max_time_step_size',
         'min_step_change_factor', 'max_step_change_factor',
         'update_interval']

    enabled: enabled = enabled
    """
    enabled child of mp_specific_time_stepping
    """
    global_courant_number: global_courant_number = global_courant_number
    """
    global_courant_number child of mp_specific_time_stepping
    """
    initial_time_step_size: initial_time_step_size = initial_time_step_size
    """
    initial_time_step_size child of mp_specific_time_stepping
    """
    fixed_time_step_size: fixed_time_step_size = fixed_time_step_size
    """
    fixed_time_step_size child of mp_specific_time_stepping
    """
    min_time_step_size: min_time_step_size = min_time_step_size
    """
    min_time_step_size child of mp_specific_time_stepping
    """
    max_time_step_size: max_time_step_size = max_time_step_size
    """
    max_time_step_size child of mp_specific_time_stepping
    """
    min_step_change_factor: min_step_change_factor = min_step_change_factor
    """
    min_step_change_factor child of mp_specific_time_stepping
    """
    max_step_change_factor: max_step_change_factor = max_step_change_factor
    """
    max_step_change_factor child of mp_specific_time_stepping
    """
    update_interval: update_interval = update_interval
    """
    update_interval child of mp_specific_time_stepping
    """
