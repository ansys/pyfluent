#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .additional_stabilization_controls import (
    additional_stabilization_controls,
)
from .execute_additional_stability_controls import (
    execute_additional_stability_controls,
)
from .execute_advanced_stabilization import execute_advanced_stabilization
from .execute_settings_optimization import execute_settings_optimization
from .velocity_limiting_treatment import velocity_limiting_treatment


class solution_stabilization(Group):
    """'solution_stabilization' child."""

    fluent_name = "solution-stabilization"

    child_names = [
        "execute_settings_optimization",
        "execute_advanced_stabilization",
        "additional_stabilization_controls",
        "execute_additional_stability_controls",
        "velocity_limiting_treatment",
    ]

    execute_settings_optimization: execute_settings_optimization = (
        execute_settings_optimization
    )
    """
    execute_settings_optimization child of solution_stabilization
    """
    execute_advanced_stabilization: execute_advanced_stabilization = (
        execute_advanced_stabilization
    )
    """
    execute_advanced_stabilization child of solution_stabilization
    """
    additional_stabilization_controls: additional_stabilization_controls = (
        additional_stabilization_controls
    )
    """
    additional_stabilization_controls child of solution_stabilization
    """
    execute_additional_stability_controls: execute_additional_stability_controls = (
        execute_additional_stability_controls
    )
    """
    execute_additional_stability_controls child of solution_stabilization
    """
    velocity_limiting_treatment: velocity_limiting_treatment = (
        velocity_limiting_treatment
    )
    """
    velocity_limiting_treatment child of solution_stabilization
    """
