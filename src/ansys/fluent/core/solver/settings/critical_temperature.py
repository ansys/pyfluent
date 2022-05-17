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
class critical_temperature(Group):
    """
    'critical_temperature' child.
    """

    fluent_name = "critical-temperature"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of critical_temperature
    """
    constant: constant = constant
    """
    constant child of critical_temperature
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of critical_temperature
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of critical_temperature
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of critical_temperature
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of critical_temperature
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of critical_temperature
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of critical_temperature
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of critical_temperature
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of critical_temperature
    """
    var_class: var_class = var_class
    """
    var_class child of critical_temperature
    """
