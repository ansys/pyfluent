#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .method import method
from .number_of_coeff import number_of_coeff
from .function_of import function_of
from .coefficients import coefficients
from .constant import constant
from .piecewise_polynomial import piecewise_polynomial
from .piecewise_linear import piecewise_linear
class viscosity_ratio(Group):
    """
    'viscosity_ratio' child.
    """

    fluent_name = "viscosity-ratio"

    child_names = \
        ['method', 'number_of_coeff', 'function_of', 'coefficients',
         'constant', 'piecewise_polynomial', 'piecewise_linear']

    method: method = method
    """
    method child of viscosity_ratio
    """
    number_of_coeff: number_of_coeff = number_of_coeff
    """
    number_of_coeff child of viscosity_ratio
    """
    function_of: function_of = function_of
    """
    function_of child of viscosity_ratio
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of viscosity_ratio
    """
    constant: constant = constant
    """
    constant child of viscosity_ratio
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of viscosity_ratio
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of viscosity_ratio
    """
