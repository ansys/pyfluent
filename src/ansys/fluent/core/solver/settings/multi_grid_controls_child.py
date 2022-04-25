#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .cycle_type import cycle_type
from .method import method
from .residual_reduction_tolerance import residual_reduction_tolerance
from .stabilization import stabilization
from .termination_criteria import termination_criteria


class multi_grid_controls_child(Group):
    """'child_object_type' of multi_grid_controls."""

    fluent_name = "child-object-type"

    child_names = [
        "cycle_type",
        "termination_criteria",
        "residual_reduction_tolerance",
        "method",
        "stabilization",
    ]

    cycle_type: cycle_type = cycle_type
    """
    cycle_type child of multi_grid_controls_child
    """
    termination_criteria: termination_criteria = termination_criteria
    """
    termination_criteria child of multi_grid_controls_child
    """
    residual_reduction_tolerance: residual_reduction_tolerance = (
        residual_reduction_tolerance
    )
    """
    residual_reduction_tolerance child of multi_grid_controls_child
    """
    method: method = method
    """
    method child of multi_grid_controls_child
    """
    stabilization: stabilization = stabilization
    """
    stabilization child of multi_grid_controls_child
    """
