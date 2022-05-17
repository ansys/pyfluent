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
class premix_heat_trans_coeff(Group):
    """
    'premix_heat_trans_coeff' child.
    """

    fluent_name = "premix-heat-trans-coeff"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of premix_heat_trans_coeff
    """
    constant: constant = constant
    """
    constant child of premix_heat_trans_coeff
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of premix_heat_trans_coeff
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of premix_heat_trans_coeff
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of premix_heat_trans_coeff
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of premix_heat_trans_coeff
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of premix_heat_trans_coeff
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of premix_heat_trans_coeff
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of premix_heat_trans_coeff
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of premix_heat_trans_coeff
    """
    var_class: var_class = var_class
    """
    var_class child of premix_heat_trans_coeff
    """
