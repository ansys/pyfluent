#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .ia_norm_min_limit import ia_norm_min_limit
from .max_rel_humidity import max_rel_humidity
from .vof_from_max_limit import vof_from_max_limit
from .vof_from_min_limit import vof_from_min_limit
from .vof_to_max_limit import vof_to_max_limit
from .vof_to_min_limit import vof_to_min_limit


class evaporation_condensation(Group):
    """'evaporation_condensation' child."""

    fluent_name = "evaporation-condensation"

    child_names = [
        "vof_from_min_limit",
        "vof_from_max_limit",
        "vof_to_min_limit",
        "vof_to_max_limit",
        "ia_norm_min_limit",
        "max_rel_humidity",
    ]

    vof_from_min_limit: vof_from_min_limit = vof_from_min_limit
    """
    vof_from_min_limit child of evaporation_condensation
    """
    vof_from_max_limit: vof_from_max_limit = vof_from_max_limit
    """
    vof_from_max_limit child of evaporation_condensation
    """
    vof_to_min_limit: vof_to_min_limit = vof_to_min_limit
    """
    vof_to_min_limit child of evaporation_condensation
    """
    vof_to_max_limit: vof_to_max_limit = vof_to_max_limit
    """
    vof_to_max_limit child of evaporation_condensation
    """
    ia_norm_min_limit: ia_norm_min_limit = ia_norm_min_limit
    """
    ia_norm_min_limit child of evaporation_condensation
    """
    max_rel_humidity: max_rel_humidity = max_rel_humidity
    """
    max_rel_humidity child of evaporation_condensation
    """
