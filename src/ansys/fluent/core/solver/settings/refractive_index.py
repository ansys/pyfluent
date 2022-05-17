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
class refractive_index(Group):
    """
    'refractive_index' child.
    """

    fluent_name = "refractive-index"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of refractive_index
    """
    constant: constant = constant
    """
    constant child of refractive_index
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of refractive_index
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of refractive_index
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of refractive_index
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of refractive_index
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of refractive_index
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of refractive_index
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of refractive_index
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of refractive_index
    """
    var_class: var_class = var_class
    """
    var_class child of refractive_index
    """
