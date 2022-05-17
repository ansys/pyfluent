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
class charge(Group):
    """
    'charge' child.
    """

    fluent_name = "charge"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of charge
    """
    constant: constant = constant
    """
    constant child of charge
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of charge
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of charge
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of charge
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of charge
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of charge
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of charge
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of charge
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of charge
    """
    var_class: var_class = var_class
    """
    var_class child of charge
    """
