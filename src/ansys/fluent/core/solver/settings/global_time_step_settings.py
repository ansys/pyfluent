#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .auto_time_size_calc_solid_zone import auto_time_size_calc_solid_zone
from .auto_time_solid_scale_factor import auto_time_solid_scale_factor
from .auto_time_step_size_cal import auto_time_step_size_cal
from .auto_time_step_size_scale_factor import auto_time_step_size_scale_factor
from .length_scale import length_scale
from .options_length_scale_calc_methods import (
    options_length_scale_calc_methods,
)
from .pseudo_time_step_size import pseudo_time_step_size
from .time_step_size_for_solid_zone import time_step_size_for_solid_zone


class global_time_step_settings(Group):
    """'global_time_step_settings' child."""

    fluent_name = "global-time-step-settings"

    child_names = [
        "auto_time_step_size_cal",
        "pseudo_time_step_size",
        "options_length_scale_calc_methods",
        "auto_time_step_size_scale_factor",
        "length_scale",
        "auto_time_size_calc_solid_zone",
        "auto_time_solid_scale_factor",
        "time_step_size_for_solid_zone",
    ]

    auto_time_step_size_cal: auto_time_step_size_cal = auto_time_step_size_cal
    """
    auto_time_step_size_cal child of global_time_step_settings
    """
    pseudo_time_step_size: pseudo_time_step_size = pseudo_time_step_size
    """
    pseudo_time_step_size child of global_time_step_settings
    """
    options_length_scale_calc_methods: options_length_scale_calc_methods = (
        options_length_scale_calc_methods
    )
    """
    options_length_scale_calc_methods child of global_time_step_settings
    """
    auto_time_step_size_scale_factor: auto_time_step_size_scale_factor = (
        auto_time_step_size_scale_factor
    )
    """
    auto_time_step_size_scale_factor child of global_time_step_settings
    """
    length_scale: length_scale = length_scale
    """
    length_scale child of global_time_step_settings
    """
    auto_time_size_calc_solid_zone: auto_time_size_calc_solid_zone = (
        auto_time_size_calc_solid_zone
    )
    """
    auto_time_size_calc_solid_zone child of global_time_step_settings
    """
    auto_time_solid_scale_factor: auto_time_solid_scale_factor = (
        auto_time_solid_scale_factor
    )
    """
    auto_time_solid_scale_factor child of global_time_step_settings
    """
    time_step_size_for_solid_zone: time_step_size_for_solid_zone = (
        time_step_size_for_solid_zone
    )
    """
    time_step_size_for_solid_zone child of global_time_step_settings
    """
