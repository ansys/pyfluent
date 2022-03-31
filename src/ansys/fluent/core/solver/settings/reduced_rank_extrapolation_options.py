#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .skip_itr import skip_itr
from .subspace_size import subspace_size


class reduced_rank_extrapolation_options(Group):
    """'reduced_rank_extrapolation_options' child."""

    fluent_name = "reduced-rank-extrapolation-options"

    child_names = ["subspace_size", "skip_itr"]

    subspace_size: subspace_size = subspace_size
    """
    subspace_size child of reduced_rank_extrapolation_options
    """
    skip_itr: skip_itr = skip_itr
    """
    skip_itr child of reduced_rank_extrapolation_options
    """
