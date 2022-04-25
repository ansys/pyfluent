#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .bubble_number_density import bubble_number_density
from .liquid_surface_tension import liquid_surface_tension
from .models import models
from .non_condensable_gas import non_condensable_gas
from .number_of_eulerian_discrete_phases import (
    number_of_eulerian_discrete_phases,
)
from .number_of_phases import number_of_phases
from .vaporization_pressure import vaporization_pressure


class multiphase(Group):
    """'multiphase' child."""

    fluent_name = "multiphase"

    child_names = [
        "models",
        "vaporization_pressure",
        "non_condensable_gas",
        "liquid_surface_tension",
        "bubble_number_density",
        "number_of_phases",
        "number_of_eulerian_discrete_phases",
    ]

    models: models = models
    """
    models child of multiphase
    """
    vaporization_pressure: vaporization_pressure = vaporization_pressure
    """
    vaporization_pressure child of multiphase
    """
    non_condensable_gas: non_condensable_gas = non_condensable_gas
    """
    non_condensable_gas child of multiphase
    """
    liquid_surface_tension: liquid_surface_tension = liquid_surface_tension
    """
    liquid_surface_tension child of multiphase
    """
    bubble_number_density: bubble_number_density = bubble_number_density
    """
    bubble_number_density child of multiphase
    """
    number_of_phases: number_of_phases = number_of_phases
    """
    number_of_phases child of multiphase
    """
    number_of_eulerian_discrete_phases: number_of_eulerian_discrete_phases = (
        number_of_eulerian_discrete_phases
    )
    """
    number_of_eulerian_discrete_phases child of multiphase
    """
