#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .smoothed_density_stabilization_method import smoothed_density_stabilization_method
from .num_of_density_smoothing import num_of_density_smoothing
from .false_time_step_linearization import false_time_step_linearization
from .auto_dt_advanced_controls import auto_dt_advanced_controls
class pseudo_transient(Group):
    """
    'pseudo_transient' child.
    """

    fluent_name = "pseudo-transient"

    child_names = \
        ['smoothed_density_stabilization_method', 'num_of_density_smoothing',
         'false_time_step_linearization', 'auto_dt_advanced_controls']

    smoothed_density_stabilization_method: smoothed_density_stabilization_method = smoothed_density_stabilization_method
    """
    smoothed_density_stabilization_method child of pseudo_transient
    """
    num_of_density_smoothing: num_of_density_smoothing = num_of_density_smoothing
    """
    num_of_density_smoothing child of pseudo_transient
    """
    false_time_step_linearization: false_time_step_linearization = false_time_step_linearization
    """
    false_time_step_linearization child of pseudo_transient
    """
    auto_dt_advanced_controls: auto_dt_advanced_controls = auto_dt_advanced_controls
    """
    auto_dt_advanced_controls child of pseudo_transient
    """
