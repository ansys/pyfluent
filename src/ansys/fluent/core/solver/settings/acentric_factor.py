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
class acentric_factor(Group):
    """
    'acentric_factor' child.
    """

    fluent_name = "acentric-factor"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of acentric_factor
    """
    constant: constant = constant
    """
    constant child of acentric_factor
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of acentric_factor
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of acentric_factor
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of acentric_factor
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of acentric_factor
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of acentric_factor
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of acentric_factor
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of acentric_factor
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of acentric_factor
    """
    var_class: var_class = var_class
    """
    var_class child of acentric_factor
    """
