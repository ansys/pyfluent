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
class dpm_bc_erosion_n(Group):
    """
    'dpm_bc_erosion_n' child.
    """

    fluent_name = "dpm-bc-erosion-n"

    child_names = \
        ['method', 'number_of_coeff', 'function_of', 'coefficients',
         'constant', 'piecewise_polynomial', 'piecewise_linear']

    method: method = method
    """
    method child of dpm_bc_erosion_n
    """
    number_of_coeff: number_of_coeff = number_of_coeff
    """
    number_of_coeff child of dpm_bc_erosion_n
    """
    function_of: function_of = function_of
    """
    function_of child of dpm_bc_erosion_n
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of dpm_bc_erosion_n
    """
    constant: constant = constant
    """
    constant child of dpm_bc_erosion_n
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of dpm_bc_erosion_n
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of dpm_bc_erosion_n
    """
