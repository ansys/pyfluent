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
class emissivity(Group):
    """
    'emissivity' child.
    """

    fluent_name = "emissivity"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of emissivity
    """
    constant: constant = constant
    """
    constant child of emissivity
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of emissivity
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of emissivity
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of emissivity
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of emissivity
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of emissivity
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of emissivity
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of emissivity
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of emissivity
    """
    var_class: var_class = var_class
    """
    var_class child of emissivity
    """
