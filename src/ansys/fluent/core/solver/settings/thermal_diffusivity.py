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
class thermal_diffusivity(Group):
    """
    'thermal_diffusivity' child.
    """

    fluent_name = "thermal-diffusivity"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of thermal_diffusivity
    """
    constant: constant = constant
    """
    constant child of thermal_diffusivity
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of thermal_diffusivity
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of thermal_diffusivity
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of thermal_diffusivity
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of thermal_diffusivity
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of thermal_diffusivity
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of thermal_diffusivity
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of thermal_diffusivity
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of thermal_diffusivity
    """
    var_class: var_class = var_class
    """
    var_class child of thermal_diffusivity
    """
