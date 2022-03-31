#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .correction_tolerance import correction_tolerance
from .expert_1 import expert
from .fast_transient_settings import fast_transient_settings
from .multi_grid import multi_grid
from .multi_stage import multi_stage
from .relaxation_method import relaxation_method


class advanced(Group):
    """'advanced' child."""

    fluent_name = "advanced"

    child_names = [
        "multi_grid",
        "multi_stage",
        "expert",
        "fast_transient_settings",
        "relaxation_method",
        "correction_tolerance",
    ]

    multi_grid: multi_grid = multi_grid
    """
    multi_grid child of advanced
    """
    multi_stage: multi_stage = multi_stage
    """
    multi_stage child of advanced
    """
    expert: expert = expert
    """
    expert child of advanced
    """
    fast_transient_settings: fast_transient_settings = fast_transient_settings
    """
    fast_transient_settings child of advanced
    """
    relaxation_method: relaxation_method = relaxation_method
    """
    relaxation_method child of advanced
    """
    correction_tolerance: correction_tolerance = correction_tolerance
    """
    correction_tolerance child of advanced
    """
