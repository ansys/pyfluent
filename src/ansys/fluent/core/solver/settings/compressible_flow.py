#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .alternate_bc_formulation import alternate_bc_formulation
from .analytical_thermodynamic_derivatives import (
    analytical_thermodynamic_derivatives,
)
from .enhanced_numerics import enhanced_numerics


class compressible_flow(Group):
    """'compressible_flow' child."""

    fluent_name = "compressible-flow"

    child_names = [
        "enhanced_numerics",
        "alternate_bc_formulation",
        "analytical_thermodynamic_derivatives",
    ]

    enhanced_numerics: enhanced_numerics = enhanced_numerics
    """
    enhanced_numerics child of compressible_flow
    """
    alternate_bc_formulation: alternate_bc_formulation = (
        alternate_bc_formulation
    )
    """
    alternate_bc_formulation child of compressible_flow
    """
    analytical_thermodynamic_derivatives: analytical_thermodynamic_derivatives = (
        analytical_thermodynamic_derivatives
    )
    """
    analytical_thermodynamic_derivatives child of compressible_flow
    """
