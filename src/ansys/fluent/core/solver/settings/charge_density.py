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
class charge_density(Group):
    """
    'charge_density' child.
    """

    fluent_name = "charge-density"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of charge_density
    """
    constant: constant = constant
    """
    constant child of charge_density
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of charge_density
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of charge_density
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of charge_density
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of charge_density
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of charge_density
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of charge_density
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of charge_density
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of charge_density
    """
    var_class: var_class = var_class
    """
    var_class child of charge_density
    """
