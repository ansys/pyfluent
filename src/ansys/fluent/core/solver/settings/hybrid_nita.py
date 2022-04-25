#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .initial_outer_iterations import initial_outer_iterations
from .instability_detector import instability_detector
from .outer_iterations import outer_iterations


class hybrid_nita(Group):
    """'hybrid_nita' child."""

    fluent_name = "hybrid-nita"

    child_names = [
        "outer_iterations",
        "initial_outer_iterations",
        "instability_detector",
    ]

    outer_iterations: outer_iterations = outer_iterations
    """
    outer_iterations child of hybrid_nita
    """
    initial_outer_iterations: initial_outer_iterations = (
        initial_outer_iterations
    )
    """
    initial_outer_iterations child of hybrid_nita
    """
    instability_detector: instability_detector = instability_detector
    """
    instability_detector child of hybrid_nita
    """
