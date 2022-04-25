#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .boundary_treatment import boundary_treatment
from .extended_boundary_treatment import extended_boundary_treatment


class nb_gradient_dbns(Group):
    """'nb_gradient_dbns' child."""

    fluent_name = "nb-gradient-dbns"

    child_names = ["boundary_treatment", "extended_boundary_treatment"]

    boundary_treatment: boundary_treatment = boundary_treatment
    """
    boundary_treatment child of nb_gradient_dbns
    """
    extended_boundary_treatment: extended_boundary_treatment = (
        extended_boundary_treatment
    )
    """
    extended_boundary_treatment child of nb_gradient_dbns
    """
