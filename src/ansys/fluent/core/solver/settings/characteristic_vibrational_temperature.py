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


class characteristic_vibrational_temperature(Group):
    """'characteristic_vibrational_temperature' child."""

    fluent_name = "characteristic-vibrational-temperature"

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
    option child of characteristic_vibrational_temperature
    """
    constant: constant = constant
    """
    constant child of characteristic_vibrational_temperature
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of characteristic_vibrational_temperature
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of characteristic_vibrational_temperature
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of characteristic_vibrational_temperature
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of characteristic_vibrational_temperature
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of characteristic_vibrational_temperature
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of characteristic_vibrational_temperature
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of characteristic_vibrational_temperature
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of characteristic_vibrational_temperature
    """
    var_class: var_class = var_class
    """
    var_class child of characteristic_vibrational_temperature
    """
