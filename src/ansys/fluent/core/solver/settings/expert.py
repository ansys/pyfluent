#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .explicit_relaxation_factor import explicit_relaxation_factor
from .under_relaxation_factor import under_relaxation_factor


class expert(Group):
    """'expert' child."""

    fluent_name = "expert"

    child_names = ["under_relaxation_factor", "explicit_relaxation_factor"]

    under_relaxation_factor: under_relaxation_factor = under_relaxation_factor
    """
    under_relaxation_factor child of expert
    """
    explicit_relaxation_factor: explicit_relaxation_factor = (
        explicit_relaxation_factor
    )
    """
    explicit_relaxation_factor child of expert
    """
