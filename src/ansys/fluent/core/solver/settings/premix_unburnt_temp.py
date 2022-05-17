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
class premix_unburnt_temp(Group):
    """
    'premix_unburnt_temp' child.
    """

    fluent_name = "premix-unburnt-temp"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of premix_unburnt_temp
    """
    constant: constant = constant
    """
    constant child of premix_unburnt_temp
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of premix_unburnt_temp
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of premix_unburnt_temp
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of premix_unburnt_temp
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of premix_unburnt_temp
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of premix_unburnt_temp
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of premix_unburnt_temp
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of premix_unburnt_temp
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of premix_unburnt_temp
    """
    var_class: var_class = var_class
    """
    var_class child of premix_unburnt_temp
    """
