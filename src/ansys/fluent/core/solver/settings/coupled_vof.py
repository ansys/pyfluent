#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .blended_treatment_for_buoyancy_forces import (
    blended_treatment_for_buoyancy_forces,
)
from .buoyancy_force_linearization import buoyancy_force_linearization


class coupled_vof(Group):
    """'coupled_vof' child."""

    fluent_name = "coupled-vof"

    child_names = [
        "buoyancy_force_linearization",
        "blended_treatment_for_buoyancy_forces",
    ]

    buoyancy_force_linearization: buoyancy_force_linearization = (
        buoyancy_force_linearization
    )
    """
    buoyancy_force_linearization child of coupled_vof
    """
    blended_treatment_for_buoyancy_forces: blended_treatment_for_buoyancy_forces = (
        blended_treatment_for_buoyancy_forces
    )
    """
    blended_treatment_for_buoyancy_forces child of coupled_vof
    """
