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


class swelling_coefficient(Group):
    """'swelling_coefficient' child."""

    fluent_name = "swelling-coefficient"

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
    option child of swelling_coefficient
    """
    constant: constant = constant
    """
    constant child of swelling_coefficient
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of swelling_coefficient
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of swelling_coefficient
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of swelling_coefficient
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of swelling_coefficient
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of swelling_coefficient
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of swelling_coefficient
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of swelling_coefficient
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of swelling_coefficient
    """
    var_class: var_class = var_class
    """
    var_class child of swelling_coefficient
    """
