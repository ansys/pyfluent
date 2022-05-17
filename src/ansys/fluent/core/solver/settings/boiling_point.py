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
class boiling_point(Group):
    """
    'boiling_point' child.
    """

    fluent_name = "boiling-point"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of boiling_point
    """
    constant: constant = constant
    """
    constant child of boiling_point
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of boiling_point
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of boiling_point
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of boiling_point
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of boiling_point
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of boiling_point
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of boiling_point
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of boiling_point
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of boiling_point
    """
    var_class: var_class = var_class
    """
    var_class child of boiling_point
    """
