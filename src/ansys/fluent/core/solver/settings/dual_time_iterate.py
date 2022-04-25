#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .incremental_time import incremental_time
from .max_iteration_per_step import max_iteration_per_step
from .num_of_post_iter_per_timestep import num_of_post_iter_per_timestep
from .number_of_time_steps import number_of_time_steps
from .number_of_total_periods import number_of_total_periods
from .postprocess import postprocess
from .total_number_of_time_steps import total_number_of_time_steps
from .total_time import total_time


class dual_time_iterate(Command):
    """Perform unsteady iterations.

    Parameters
    ----------
        number_of_total_periods : int
            Set number of total periods.
        number_of_time_steps : int
            Set inceremtal number of Time steps.
        total_number_of_time_steps : int
            Set total number of Time steps.
        total_time : real
            Set Total Simulation Time.
        incremental_time : real
            Set Incremental Time.
        max_iteration_per_step : int
            Set Maximum Number of iterations per time step.
        postprocess : bool
            Enable/Disable Postprocess pollutant solution?.
        num_of_post_iter_per_timestep : int
            Set Number of post-processing iterations per time step.
    """

    fluent_name = "dual-time-iterate"

    argument_names = [
        "number_of_total_periods",
        "number_of_time_steps",
        "total_number_of_time_steps",
        "total_time",
        "incremental_time",
        "max_iteration_per_step",
        "postprocess",
        "num_of_post_iter_per_timestep",
    ]

    number_of_total_periods: number_of_total_periods = number_of_total_periods
    """
    number_of_total_periods argument of dual_time_iterate
    """
    number_of_time_steps: number_of_time_steps = number_of_time_steps
    """
    number_of_time_steps argument of dual_time_iterate
    """
    total_number_of_time_steps: total_number_of_time_steps = (
        total_number_of_time_steps
    )
    """
    total_number_of_time_steps argument of dual_time_iterate
    """
    total_time: total_time = total_time
    """
    total_time argument of dual_time_iterate
    """
    incremental_time: incremental_time = incremental_time
    """
    incremental_time argument of dual_time_iterate
    """
    max_iteration_per_step: max_iteration_per_step = max_iteration_per_step
    """
    max_iteration_per_step argument of dual_time_iterate
    """
    postprocess: postprocess = postprocess
    """
    postprocess argument of dual_time_iterate
    """
    num_of_post_iter_per_timestep: num_of_post_iter_per_timestep = (
        num_of_post_iter_per_timestep
    )
    """
    num_of_post_iter_per_timestep argument of dual_time_iterate
    """
