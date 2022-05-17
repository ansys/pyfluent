#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .cavitation import cavitation
from .evaporation_condensation import evaporation_condensation
from .boiling import boiling
from .area_density_1 import area_density
from .alternative_energy_treatment import alternative_energy_treatment
class heat_mass_transfer(Group):
    """
    'heat_mass_transfer' child.
    """

    fluent_name = "heat-mass-transfer"

    child_names = \
        ['cavitation', 'evaporation_condensation', 'boiling', 'area_density',
         'alternative_energy_treatment']

    cavitation: cavitation = cavitation
    """
    cavitation child of heat_mass_transfer
    """
    evaporation_condensation: evaporation_condensation = evaporation_condensation
    """
    evaporation_condensation child of heat_mass_transfer
    """
    boiling: boiling = boiling
    """
    boiling child of heat_mass_transfer
    """
    area_density: area_density = area_density
    """
    area_density child of heat_mass_transfer
    """
    alternative_energy_treatment: alternative_energy_treatment = alternative_energy_treatment
    """
    alternative_energy_treatment child of heat_mass_transfer
    """
