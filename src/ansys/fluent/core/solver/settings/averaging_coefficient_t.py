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


class averaging_coefficient_t(Group):
    """'averaging_coefficient_t' child."""

    fluent_name = "averaging-coefficient-t"

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
    option child of averaging_coefficient_t
    """
    constant: constant = constant
    """
    constant child of averaging_coefficient_t
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of averaging_coefficient_t
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of averaging_coefficient_t
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of averaging_coefficient_t
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of averaging_coefficient_t
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of averaging_coefficient_t
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of averaging_coefficient_t
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of averaging_coefficient_t
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of averaging_coefficient_t
    """
    var_class: var_class = var_class
    """
    var_class child of averaging_coefficient_t
    """
