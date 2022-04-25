#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .amg_controls import amg_controls
from .limits_1 import limits
from .multi_stage_parameter import multi_stage_parameter
from .reset_pseudo_time_method_equations import (
    reset_pseudo_time_method_equations,
)
from .reset_pseudo_time_method_generic import reset_pseudo_time_method_generic
from .reset_pseudo_time_method_relaxations import (
    reset_pseudo_time_method_relaxations,
)
from .reset_pseudo_time_method_scale_factors import (
    reset_pseudo_time_method_scale_factors,
)
from .solution_controls import solution_controls


class set_controls_to_default(Group):
    """'set_controls_to_default' child."""

    fluent_name = "set-controls-to-default"

    command_names = [
        "solution_controls",
        "amg_controls",
        "multi_stage_parameter",
        "limits",
        "reset_pseudo_time_method_generic",
        "reset_pseudo_time_method_equations",
        "reset_pseudo_time_method_relaxations",
        "reset_pseudo_time_method_scale_factors",
    ]

    solution_controls: solution_controls = solution_controls
    """
    solution_controls command of set_controls_to_default
    """
    amg_controls: amg_controls = amg_controls
    """
    amg_controls command of set_controls_to_default
    """
    multi_stage_parameter: multi_stage_parameter = multi_stage_parameter
    """
    multi_stage_parameter command of set_controls_to_default
    """
    limits: limits = limits
    """
    limits command of set_controls_to_default
    """
    reset_pseudo_time_method_generic: reset_pseudo_time_method_generic = (
        reset_pseudo_time_method_generic
    )
    """
    reset_pseudo_time_method_generic command of set_controls_to_default
    """
    reset_pseudo_time_method_equations: reset_pseudo_time_method_equations = (
        reset_pseudo_time_method_equations
    )
    """
    reset_pseudo_time_method_equations command of set_controls_to_default
    """
    reset_pseudo_time_method_relaxations: reset_pseudo_time_method_relaxations = (
        reset_pseudo_time_method_relaxations
    )
    """
    reset_pseudo_time_method_relaxations command of set_controls_to_default
    """
    reset_pseudo_time_method_scale_factors: reset_pseudo_time_method_scale_factors = (
        reset_pseudo_time_method_scale_factors
    )
    """
    reset_pseudo_time_method_scale_factors command of set_controls_to_default
    """
