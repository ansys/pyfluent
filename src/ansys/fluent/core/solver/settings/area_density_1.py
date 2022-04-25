#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .ia_grad_sym import ia_grad_sym
from .vof_min_seeding import vof_min_seeding


class area_density(Group):
    """'area_density' child."""

    fluent_name = "area-density"

    child_names = ["vof_min_seeding", "ia_grad_sym"]

    vof_min_seeding: vof_min_seeding = vof_min_seeding
    """
    vof_min_seeding child of area_density
    """
    ia_grad_sym: ia_grad_sym = ia_grad_sym
    """
    ia_grad_sym child of area_density
    """
