#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .viscous_terms import viscous_terms
from .species_reactions import species_reactions
from .set_turbulent_viscosity_ratio import set_turbulent_viscosity_ratio
class fmg_options(Group):
    """
    'fmg_options' child.
    """

    fluent_name = "fmg-options"

    child_names = \
        ['viscous_terms', 'species_reactions',
         'set_turbulent_viscosity_ratio']

    viscous_terms: viscous_terms = viscous_terms
    """
    viscous_terms child of fmg_options
    """
    species_reactions: species_reactions = species_reactions
    """
    species_reactions child of fmg_options
    """
    set_turbulent_viscosity_ratio: set_turbulent_viscosity_ratio = set_turbulent_viscosity_ratio
    """
    set_turbulent_viscosity_ratio child of fmg_options
    """
