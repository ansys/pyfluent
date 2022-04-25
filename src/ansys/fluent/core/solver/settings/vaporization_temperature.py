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


class vaporization_temperature(Group):
    """'vaporization_temperature' child."""

    fluent_name = "vaporization-temperature"

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
    option child of vaporization_temperature
    """
    constant: constant = constant
    """
    constant child of vaporization_temperature
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of vaporization_temperature
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of vaporization_temperature
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of vaporization_temperature
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of vaporization_temperature
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of vaporization_temperature
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of vaporization_temperature
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of vaporization_temperature
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of vaporization_temperature
    """
    var_class: var_class = var_class
    """
    var_class child of vaporization_temperature
    """
