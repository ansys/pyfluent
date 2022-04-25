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


class absorption_coefficient(Group):
    """'absorption_coefficient' child."""

    fluent_name = "absorption-coefficient"

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
    option child of absorption_coefficient
    """
    constant: constant = constant
    """
    constant child of absorption_coefficient
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of absorption_coefficient
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of absorption_coefficient
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of absorption_coefficient
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of absorption_coefficient
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of absorption_coefficient
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of absorption_coefficient
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of absorption_coefficient
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of absorption_coefficient
    """
    var_class: var_class = var_class
    """
    var_class child of absorption_coefficient
    """
