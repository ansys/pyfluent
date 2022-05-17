#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enabled import enabled
from .viscous_dissipation import viscous_dissipation
from .pressure_work import pressure_work
from .kinetic_energy import kinetic_energy
from .inlet_diffusion import inlet_diffusion
class energy(Group):
    """
    'energy' child.
    """

    fluent_name = "energy"

    child_names = \
        ['enabled', 'viscous_dissipation', 'pressure_work', 'kinetic_energy',
         'inlet_diffusion']

    enabled: enabled = enabled
    """
    enabled child of energy
    """
    viscous_dissipation: viscous_dissipation = viscous_dissipation
    """
    viscous_dissipation child of energy
    """
    pressure_work: pressure_work = pressure_work
    """
    pressure_work child of energy
    """
    kinetic_energy: kinetic_energy = kinetic_energy
    """
    kinetic_energy child of energy
    """
    inlet_diffusion: inlet_diffusion = inlet_diffusion
    """
    inlet_diffusion child of energy
    """
