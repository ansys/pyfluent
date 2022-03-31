#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .cell_to_limiting import cell_to_limiting
from .limiter_filter import limiter_filter
from .limiter_type import limiter_type


class spatial_discretization_limiter(Group):
    """'spatial_discretization_limiter' child."""

    fluent_name = "spatial-discretization-limiter"

    child_names = ["limiter_type", "cell_to_limiting", "limiter_filter"]

    limiter_type: limiter_type = limiter_type
    """
    limiter_type child of spatial_discretization_limiter
    """
    cell_to_limiting: cell_to_limiting = cell_to_limiting
    """
    cell_to_limiting child of spatial_discretization_limiter
    """
    limiter_filter: limiter_filter = limiter_filter
    """
    limiter_filter child of spatial_discretization_limiter
    """
