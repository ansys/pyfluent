#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .boussinesq import boussinesq
from .coefficients import coefficients
from .number_of_coefficients import number_of_coefficients
from .piecewise_polynomial import piecewise_polynomial
from .nasa_9_piecewise_polynomial import nasa_9_piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .anisotropic import anisotropic
from .orthotropic import orthotropic
from .var_class import var_class
class diffusivity_reference_pressure(Group):
    """
    'diffusivity_reference_pressure' child.
    """

    fluent_name = "diffusivity-reference-pressure"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of diffusivity_reference_pressure
    """
    constant: constant = constant
    """
    constant child of diffusivity_reference_pressure
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of diffusivity_reference_pressure
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of diffusivity_reference_pressure
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of diffusivity_reference_pressure
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of diffusivity_reference_pressure
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of diffusivity_reference_pressure
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of diffusivity_reference_pressure
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of diffusivity_reference_pressure
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of diffusivity_reference_pressure
    """
    var_class: var_class = var_class
    """
    var_class child of diffusivity_reference_pressure
    """
