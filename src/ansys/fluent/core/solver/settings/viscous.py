#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .model import model
from .options import options
from .spalart_allmaras_production import spalart_allmaras_production
from .k_epsilon_model import k_epsilon_model
from .k_omega_model import k_omega_model
from .k_omega_options import k_omega_options
from .rng_options import rng_options
from .near_wall_treatment import near_wall_treatment
from .transition_sst_options import transition_sst_options
from .reynolds_stress_model import reynolds_stress_model
from .subgrid_scale_model import subgrid_scale_model
from .les_model_options import les_model_options
from .reynolds_stress_options import reynolds_stress_options
from .enhanced_wall_treatment_options import enhanced_wall_treatment_options
from .rans_model import rans_model
class viscous(Group):
    """
    'viscous' child.
    """

    fluent_name = "viscous"

    child_names = \
        ['model', 'options', 'spalart_allmaras_production', 'k_epsilon_model',
         'k_omega_model', 'k_omega_options', 'rng_options',
         'near_wall_treatment', 'transition_sst_options',
         'reynolds_stress_model', 'subgrid_scale_model', 'les_model_options',
         'reynolds_stress_options', 'enhanced_wall_treatment_options',
         'rans_model']

    model: model = model
    """
    model child of viscous
    """
    options: options = options
    """
    options child of viscous
    """
    spalart_allmaras_production: spalart_allmaras_production = spalart_allmaras_production
    """
    spalart_allmaras_production child of viscous
    """
    k_epsilon_model: k_epsilon_model = k_epsilon_model
    """
    k_epsilon_model child of viscous
    """
    k_omega_model: k_omega_model = k_omega_model
    """
    k_omega_model child of viscous
    """
    k_omega_options: k_omega_options = k_omega_options
    """
    k_omega_options child of viscous
    """
    rng_options: rng_options = rng_options
    """
    rng_options child of viscous
    """
    near_wall_treatment: near_wall_treatment = near_wall_treatment
    """
    near_wall_treatment child of viscous
    """
    transition_sst_options: transition_sst_options = transition_sst_options
    """
    transition_sst_options child of viscous
    """
    reynolds_stress_model: reynolds_stress_model = reynolds_stress_model
    """
    reynolds_stress_model child of viscous
    """
    subgrid_scale_model: subgrid_scale_model = subgrid_scale_model
    """
    subgrid_scale_model child of viscous
    """
    les_model_options: les_model_options = les_model_options
    """
    les_model_options child of viscous
    """
    reynolds_stress_options: reynolds_stress_options = reynolds_stress_options
    """
    reynolds_stress_options child of viscous
    """
    enhanced_wall_treatment_options: enhanced_wall_treatment_options = enhanced_wall_treatment_options
    """
    enhanced_wall_treatment_options child of viscous
    """
    rans_model: rans_model = rans_model
    """
    rans_model child of viscous
    """
