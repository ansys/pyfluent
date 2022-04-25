#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .coefficients import coefficients
from .constant import constant
from .function_of import function_of
from .method import method
from .number_of_coeff import number_of_coeff
from .piecewise_linear import piecewise_linear
from .piecewise_polynomial import piecewise_polynomial


class a(Group):
    """'a' child."""

    fluent_name = "a"

    child_names = [
        "method",
        "number_of_coeff",
        "function_of",
        "coefficients",
        "constant",
        "piecewise_polynomial",
        "piecewise_linear",
    ]

    method: method = method
    """
    method child of a
    """
    number_of_coeff: number_of_coeff = number_of_coeff
    """
    number_of_coeff child of a
    """
    function_of: function_of = function_of
    """
    function_of child of a
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of a
    """
    constant: constant = constant
    """
    constant child of a
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of a
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of a
    """
