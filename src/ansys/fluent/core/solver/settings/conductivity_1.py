#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .coefficients import coefficients
from .constant import constant
from .number_of_coefficients import number_of_coefficients
from .option import option
from .piecewise_linear import piecewise_linear
from .piecewise_polynomial import piecewise_polynomial


class conductivity_1(Group):
    """'conductivity_1' child."""

    fluent_name = "conductivity-1"

    child_names = [
        "option",
        "constant",
        "coefficients",
        "number_of_coefficients",
        "piecewise_linear",
        "piecewise_polynomial",
    ]

    option: option = option
    """
    option child of conductivity_1
    """
    constant: constant = constant
    """
    constant child of conductivity_1
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of conductivity_1
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of conductivity_1
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of conductivity_1
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of conductivity_1
    """
