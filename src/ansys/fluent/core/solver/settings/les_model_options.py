#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .dynamic_stress import dynamic_stress
from .dynamic_energy_flux import dynamic_energy_flux
from .dynamic_scalar_flux import dynamic_scalar_flux
from .subgrid_dynamic_fvar import subgrid_dynamic_fvar
class les_model_options(Group):
    """
    'les_model_options' child.
    """

    fluent_name = "les-model-options"

    child_names = \
        ['dynamic_stress', 'dynamic_energy_flux', 'dynamic_scalar_flux',
         'subgrid_dynamic_fvar']

    dynamic_stress: dynamic_stress = dynamic_stress
    """
    dynamic_stress child of les_model_options
    """
    dynamic_energy_flux: dynamic_energy_flux = dynamic_energy_flux
    """
    dynamic_energy_flux child of les_model_options
    """
    dynamic_scalar_flux: dynamic_scalar_flux = dynamic_scalar_flux
    """
    dynamic_scalar_flux child of les_model_options
    """
    subgrid_dynamic_fvar: subgrid_dynamic_fvar = subgrid_dynamic_fvar
    """
    subgrid_dynamic_fvar child of les_model_options
    """
