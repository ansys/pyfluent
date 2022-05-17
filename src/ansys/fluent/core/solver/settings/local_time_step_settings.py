#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .pseudo_time_courant_number import pseudo_time_courant_number
from .pseudo_time_step_method_solid_zone import pseudo_time_step_method_solid_zone
from .time_step_size_scale_factor import time_step_size_scale_factor
class local_time_step_settings(Group):
    """
    'local_time_step_settings' child.
    """

    fluent_name = "local-time-step-settings"

    child_names = \
        ['pseudo_time_courant_number', 'pseudo_time_step_method_solid_zone',
         'time_step_size_scale_factor']

    pseudo_time_courant_number: pseudo_time_courant_number = pseudo_time_courant_number
    """
    pseudo_time_courant_number child of local_time_step_settings
    """
    pseudo_time_step_method_solid_zone: pseudo_time_step_method_solid_zone = pseudo_time_step_method_solid_zone
    """
    pseudo_time_step_method_solid_zone child of local_time_step_settings
    """
    time_step_size_scale_factor: time_step_size_scale_factor = time_step_size_scale_factor
    """
    time_step_size_scale_factor child of local_time_step_settings
    """
