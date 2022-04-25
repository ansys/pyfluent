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


class vapor_pressure(Group):
    """'vapor_pressure' child."""

    fluent_name = "vapor-pressure"

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
    option child of vapor_pressure
    """
    constant: constant = constant
    """
    constant child of vapor_pressure
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of vapor_pressure
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of vapor_pressure
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of vapor_pressure
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of vapor_pressure
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of vapor_pressure
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of vapor_pressure
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of vapor_pressure
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of vapor_pressure
    """
    var_class: var_class = var_class
    """
    var_class child of vapor_pressure
    """
