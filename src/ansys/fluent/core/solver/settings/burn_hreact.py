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
class burn_hreact(Group):
    """
    'burn_hreact' child.
    """

    fluent_name = "burn-hreact"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of burn_hreact
    """
    constant: constant = constant
    """
    constant child of burn_hreact
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of burn_hreact
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of burn_hreact
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of burn_hreact
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of burn_hreact
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of burn_hreact
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of burn_hreact
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of burn_hreact
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of burn_hreact
    """
    var_class: var_class = var_class
    """
    var_class child of burn_hreact
    """
