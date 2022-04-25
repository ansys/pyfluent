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


class velocity_accom_coefficient(Group):
    """'velocity_accom_coefficient' child."""

    fluent_name = "velocity-accom-coefficient"

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
    option child of velocity_accom_coefficient
    """
    constant: constant = constant
    """
    constant child of velocity_accom_coefficient
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of velocity_accom_coefficient
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of velocity_accom_coefficient
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of velocity_accom_coefficient
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of velocity_accom_coefficient
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of velocity_accom_coefficient
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of velocity_accom_coefficient
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of velocity_accom_coefficient
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of velocity_accom_coefficient
    """
    var_class: var_class = var_class
    """
    var_class child of velocity_accom_coefficient
    """
