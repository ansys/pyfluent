#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .expert_3 import expert
from .high_order_pressure import high_order_pressure
from .interpolation_method import interpolation_method
from .orphan_cell_treatment import orphan_cell_treatment


class overset(Group):
    """'overset' child."""

    fluent_name = "overset"

    child_names = [
        "high_order_pressure",
        "interpolation_method",
        "orphan_cell_treatment",
        "expert",
    ]

    high_order_pressure: high_order_pressure = high_order_pressure
    """
    high_order_pressure child of overset
    """
    interpolation_method: interpolation_method = interpolation_method
    """
    interpolation_method child of overset
    """
    orphan_cell_treatment: orphan_cell_treatment = orphan_cell_treatment
    """
    orphan_cell_treatment child of overset
    """
    expert: expert = expert
    """
    expert child of overset
    """
