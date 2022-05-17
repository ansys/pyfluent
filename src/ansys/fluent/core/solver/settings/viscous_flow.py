#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .viscosity_averaging import viscosity_averaging
from .turb_visc_based_damping import turb_visc_based_damping
from .density_func_expo import density_func_expo
from .density_ratio_cutoff import density_ratio_cutoff
from .interfacial_artificial_viscosity import interfacial_artificial_viscosity
class viscous_flow(Group):
    """
    'viscous_flow' child.
    """

    fluent_name = "viscous-flow"

    child_names = \
        ['viscosity_averaging', 'turb_visc_based_damping',
         'density_func_expo', 'density_ratio_cutoff',
         'interfacial_artificial_viscosity']

    viscosity_averaging: viscosity_averaging = viscosity_averaging
    """
    viscosity_averaging child of viscous_flow
    """
    turb_visc_based_damping: turb_visc_based_damping = turb_visc_based_damping
    """
    turb_visc_based_damping child of viscous_flow
    """
    density_func_expo: density_func_expo = density_func_expo
    """
    density_func_expo child of viscous_flow
    """
    density_ratio_cutoff: density_ratio_cutoff = density_ratio_cutoff
    """
    density_ratio_cutoff child of viscous_flow
    """
    interfacial_artificial_viscosity: interfacial_artificial_viscosity = interfacial_artificial_viscosity
    """
    interfacial_artificial_viscosity child of viscous_flow
    """
