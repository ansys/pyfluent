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
class eutectic_mf(Group):
    """
    'eutectic_mf' child.
    """

    fluent_name = "eutectic-mf"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of eutectic_mf
    """
    constant: constant = constant
    """
    constant child of eutectic_mf
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of eutectic_mf
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of eutectic_mf
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of eutectic_mf
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of eutectic_mf
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of eutectic_mf
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of eutectic_mf
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of eutectic_mf
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of eutectic_mf
    """
    var_class: var_class = var_class
    """
    var_class child of eutectic_mf
    """
