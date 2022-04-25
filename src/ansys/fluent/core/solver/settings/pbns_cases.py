#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .flux_auto_select import flux_auto_select
from .flux_type_1 import flux_type


class pbns_cases(Group):
    """'pbns_cases' child."""

    fluent_name = "pbns_cases"

    child_names = ["flux_auto_select", "flux_type"]

    flux_auto_select: flux_auto_select = flux_auto_select
    """
    flux_auto_select child of pbns_cases
    """
    flux_type: flux_type = flux_type
    """
    flux_type child of pbns_cases
    """
