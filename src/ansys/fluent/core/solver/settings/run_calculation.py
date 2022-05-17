#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .adaptive_time_stepping import adaptive_time_stepping
from .cfl_based_adaptive_time_stepping import cfl_based_adaptive_time_stepping
from .data_sampling_1 import data_sampling
from .transient_controls import transient_controls
from .dual_time_iterate import dual_time_iterate
from .iterate import iterate
class run_calculation(Group):
    """
    'run_calculation' child.
    """

    fluent_name = "run-calculation"

    child_names = \
        ['adaptive_time_stepping', 'cfl_based_adaptive_time_stepping',
         'data_sampling', 'transient_controls']

    adaptive_time_stepping: adaptive_time_stepping = adaptive_time_stepping
    """
    adaptive_time_stepping child of run_calculation
    """
    cfl_based_adaptive_time_stepping: cfl_based_adaptive_time_stepping = cfl_based_adaptive_time_stepping
    """
    cfl_based_adaptive_time_stepping child of run_calculation
    """
    data_sampling: data_sampling = data_sampling
    """
    data_sampling child of run_calculation
    """
    transient_controls: transient_controls = transient_controls
    """
    transient_controls child of run_calculation
    """
    command_names = \
        ['dual_time_iterate', 'iterate']

    dual_time_iterate: dual_time_iterate = dual_time_iterate
    """
    dual_time_iterate command of run_calculation
    """
    iterate: iterate = iterate
    """
    iterate command of run_calculation
    """
