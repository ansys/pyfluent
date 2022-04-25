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


class liquidus_slope(Group):
    """'liquidus_slope' child."""

    fluent_name = "liquidus-slope"

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
    option child of liquidus_slope
    """
    constant: constant = constant
    """
    constant child of liquidus_slope
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of liquidus_slope
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of liquidus_slope
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of liquidus_slope
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of liquidus_slope
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of liquidus_slope
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of liquidus_slope
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of liquidus_slope
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of liquidus_slope
    """
    var_class: var_class = var_class
    """
    var_class child of liquidus_slope
    """
