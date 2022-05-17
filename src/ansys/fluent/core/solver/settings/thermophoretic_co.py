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
class thermophoretic_co(Group):
    """
    'thermophoretic_co' child.
    """

    fluent_name = "thermophoretic-co"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of thermophoretic_co
    """
    constant: constant = constant
    """
    constant child of thermophoretic_co
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of thermophoretic_co
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of thermophoretic_co
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of thermophoretic_co
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of thermophoretic_co
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of thermophoretic_co
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of thermophoretic_co
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of thermophoretic_co
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of thermophoretic_co
    """
    var_class: var_class = var_class
    """
    var_class child of thermophoretic_co
    """
