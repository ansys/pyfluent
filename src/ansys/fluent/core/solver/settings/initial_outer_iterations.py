#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .initial_outer_iter import initial_outer_iter
from .initial_time_steps import initial_time_steps


class initial_outer_iterations(Group):
    """'initial_outer_iterations' child."""

    fluent_name = "initial-outer-iterations"

    child_names = ["initial_time_steps", "initial_outer_iter"]

    initial_time_steps: initial_time_steps = initial_time_steps
    """
    initial_time_steps child of initial_outer_iterations
    """
    initial_outer_iter: initial_outer_iter = initial_outer_iter
    """
    initial_outer_iter child of initial_outer_iterations
    """
