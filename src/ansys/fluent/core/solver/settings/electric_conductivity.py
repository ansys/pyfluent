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
class electric_conductivity(Group):
    """
    'electric_conductivity' child.
    """

    fluent_name = "electric-conductivity"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of electric_conductivity
    """
    constant: constant = constant
    """
    constant child of electric_conductivity
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of electric_conductivity
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of electric_conductivity
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of electric_conductivity
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of electric_conductivity
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of electric_conductivity
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of electric_conductivity
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of electric_conductivity
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of electric_conductivity
    """
    var_class: var_class = var_class
    """
    var_class child of electric_conductivity
    """
