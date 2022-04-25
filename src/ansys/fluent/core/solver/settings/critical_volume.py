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


class critical_volume(Group):
    """'critical_volume' child."""

    fluent_name = "critical-volume"

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
    option child of critical_volume
    """
    constant: constant = constant
    """
    constant child of critical_volume
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of critical_volume
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of critical_volume
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of critical_volume
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of critical_volume
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of critical_volume
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of critical_volume
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of critical_volume
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of critical_volume
    """
    var_class: var_class = var_class
    """
    var_class child of critical_volume
    """
