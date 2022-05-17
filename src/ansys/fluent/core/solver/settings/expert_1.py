#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .spatial_discretization_limiter import spatial_discretization_limiter
class expert(Group):
    """
    'expert' child.
    """

    fluent_name = "expert"

    child_names = \
        ['spatial_discretization_limiter']

    spatial_discretization_limiter: spatial_discretization_limiter = spatial_discretization_limiter
    """
    spatial_discretization_limiter child of expert
    """
