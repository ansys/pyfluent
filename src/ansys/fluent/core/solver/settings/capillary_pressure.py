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


class capillary_pressure(Group):
    """'capillary_pressure' child."""

    fluent_name = "capillary-pressure"

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
    method child of capillary_pressure
    """
    number_of_coeff: number_of_coeff = number_of_coeff
    """
    number_of_coeff child of capillary_pressure
    """
    function_of: function_of = function_of
    """
    function_of child of capillary_pressure
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of capillary_pressure
    """
    constant: constant = constant
    """
    constant child of capillary_pressure
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of capillary_pressure
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of capillary_pressure
    """
