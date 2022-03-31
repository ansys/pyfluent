#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .anisotropic import anisotropic
from .boussinesq import boussinesq
from .coefficients import coefficients
from .constant import constant
from .nasa_9_piecewise_polynomial import nasa_9_piecewise_polynomial
from .number_of_coefficients import number_of_coefficients
from .option import option
from .orthotropic import orthotropic
from .piecewise_linear import piecewise_linear
from .piecewise_polynomial import piecewise_polynomial
from .var_class import var_class


class averaging_coefficient_y(Group):
    """'averaging_coefficient_y' child."""

    fluent_name = "averaging-coefficient-y"

    child_names = [
        "option",
        "constant",
        "boussinesq",
        "coefficients",
        "number_of_coefficients",
        "piecewise_polynomial",
        "nasa_9_piecewise_polynomial",
        "piecewise_linear",
        "anisotropic",
        "orthotropic",
        "var_class",
    ]

    option: option = option
    """
    option child of averaging_coefficient_y
    """
    constant: constant = constant
    """
    constant child of averaging_coefficient_y
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of averaging_coefficient_y
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of averaging_coefficient_y
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of averaging_coefficient_y
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of averaging_coefficient_y
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of averaging_coefficient_y
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of averaging_coefficient_y
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of averaging_coefficient_y
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of averaging_coefficient_y
    """
    var_class: var_class = var_class
    """
    var_class child of averaging_coefficient_y
    """
