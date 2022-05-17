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
class dpm_bc_norm_coeff(Group):
    """
    'dpm_bc_norm_coeff' child.
    """

    fluent_name = "dpm-bc-norm-coeff"

    child_names = \
        ['method', 'number_of_coeff', 'function_of', 'coefficients',
         'constant', 'piecewise_polynomial', 'piecewise_linear']

    method: method = method
    """
    method child of dpm_bc_norm_coeff
    """
    number_of_coeff: number_of_coeff = number_of_coeff
    """
    number_of_coeff child of dpm_bc_norm_coeff
    """
    function_of: function_of = function_of
    """
    function_of child of dpm_bc_norm_coeff
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of dpm_bc_norm_coeff
    """
    constant: constant = constant
    """
    constant child of dpm_bc_norm_coeff
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of dpm_bc_norm_coeff
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of dpm_bc_norm_coeff
    """
