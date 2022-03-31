#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .cfl_based_time_stepping import cfl_based_time_stepping
from .cfl_type import cfl_type
from .control_time_step_size_variation import control_time_step_size_variation
from .error_based_time_stepping import error_based_time_stepping
from .extrapolate_vars import extrapolate_vars
from .incremental_time import incremental_time
from .max_flow_time import max_flow_time
from .max_iterations_per_time_step import max_iterations_per_time_step
from .method import method
from .mp_specific_time_stepping import mp_specific_time_stepping
from .number_of_time_steps import number_of_time_steps
from .predict_next import predict_next
from .rotating_mesh_flow_predictor import rotating_mesh_flow_predictor
from .solution_status import solution_status
from .specified_time_step import specified_time_step
from .time_step_size import time_step_size
from .total_number_of_time_steps import total_number_of_time_steps
from .total_time import total_time
from .type_1 import type
from .udf_hook import udf_hook
from .undo_timestep import undo_timestep
from .use_average_cfl import use_average_cfl


class transient_controls(Group):
    """'transient_controls' child."""

    fluent_name = "transient-controls"

    child_names = [
        "type",
        "method",
        "specified_time_step",
        "incremental_time",
        "max_iterations_per_time_step",
        "number_of_time_steps",
        "total_number_of_time_steps",
        "total_time",
        "time_step_size",
        "solution_status",
        "extrapolate_vars",
        "max_flow_time",
        "control_time_step_size_variation",
        "use_average_cfl",
        "cfl_type",
        "cfl_based_time_stepping",
        "error_based_time_stepping",
        "undo_timestep",
        "predict_next",
        "rotating_mesh_flow_predictor",
        "mp_specific_time_stepping",
        "udf_hook",
    ]

    type: type = type
    """
    type child of transient_controls
    """
    method: method = method
    """
    method child of transient_controls
    """
    specified_time_step: specified_time_step = specified_time_step
    """
    specified_time_step child of transient_controls
    """
    incremental_time: incremental_time = incremental_time
    """
    incremental_time child of transient_controls
    """
    max_iterations_per_time_step: max_iterations_per_time_step = (
        max_iterations_per_time_step
    )
    """
    max_iterations_per_time_step child of transient_controls
    """
    number_of_time_steps: number_of_time_steps = number_of_time_steps
    """
    number_of_time_steps child of transient_controls
    """
    total_number_of_time_steps: total_number_of_time_steps = (
        total_number_of_time_steps
    )
    """
    total_number_of_time_steps child of transient_controls
    """
    total_time: total_time = total_time
    """
    total_time child of transient_controls
    """
    time_step_size: time_step_size = time_step_size
    """
    time_step_size child of transient_controls
    """
    solution_status: solution_status = solution_status
    """
    solution_status child of transient_controls
    """
    extrapolate_vars: extrapolate_vars = extrapolate_vars
    """
    extrapolate_vars child of transient_controls
    """
    max_flow_time: max_flow_time = max_flow_time
    """
    max_flow_time child of transient_controls
    """
    control_time_step_size_variation: control_time_step_size_variation = (
        control_time_step_size_variation
    )
    """
    control_time_step_size_variation child of transient_controls
    """
    use_average_cfl: use_average_cfl = use_average_cfl
    """
    use_average_cfl child of transient_controls
    """
    cfl_type: cfl_type = cfl_type
    """
    cfl_type child of transient_controls
    """
    cfl_based_time_stepping: cfl_based_time_stepping = cfl_based_time_stepping
    """
    cfl_based_time_stepping child of transient_controls
    """
    error_based_time_stepping: error_based_time_stepping = (
        error_based_time_stepping
    )
    """
    error_based_time_stepping child of transient_controls
    """
    undo_timestep: undo_timestep = undo_timestep
    """
    undo_timestep child of transient_controls
    """
    predict_next: predict_next = predict_next
    """
    predict_next child of transient_controls
    """
    rotating_mesh_flow_predictor: rotating_mesh_flow_predictor = (
        rotating_mesh_flow_predictor
    )
    """
    rotating_mesh_flow_predictor child of transient_controls
    """
    mp_specific_time_stepping: mp_specific_time_stepping = (
        mp_specific_time_stepping
    )
    """
    mp_specific_time_stepping child of transient_controls
    """
    udf_hook: udf_hook = udf_hook
    """
    udf_hook child of transient_controls
    """
