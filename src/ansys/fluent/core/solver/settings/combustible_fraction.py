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


class combustible_fraction(Group):
    """'combustible_fraction' child."""

    fluent_name = "combustible-fraction"

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
    option child of combustible_fraction
    """
    constant: constant = constant
    """
    constant child of combustible_fraction
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of combustible_fraction
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of combustible_fraction
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of combustible_fraction
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of combustible_fraction
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of combustible_fraction
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of combustible_fraction
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of combustible_fraction
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of combustible_fraction
    """
    var_class: var_class = var_class
    """
    var_class child of combustible_fraction
    """
