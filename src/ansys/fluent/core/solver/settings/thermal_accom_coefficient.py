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


class thermal_accom_coefficient(Group):
    """'thermal_accom_coefficient' child."""

    fluent_name = "thermal-accom-coefficient"

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
    option child of thermal_accom_coefficient
    """
    constant: constant = constant
    """
    constant child of thermal_accom_coefficient
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of thermal_accom_coefficient
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of thermal_accom_coefficient
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of thermal_accom_coefficient
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of thermal_accom_coefficient
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of thermal_accom_coefficient
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of thermal_accom_coefficient
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of thermal_accom_coefficient
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of thermal_accom_coefficient
    """
    var_class: var_class = var_class
    """
    var_class child of thermal_accom_coefficient
    """
