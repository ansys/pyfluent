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


class dpm_surften(Group):
    """'dpm_surften' child."""

    fluent_name = "dpm-surften"

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
    option child of dpm_surften
    """
    constant: constant = constant
    """
    constant child of dpm_surften
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of dpm_surften
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of dpm_surften
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of dpm_surften
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of dpm_surften
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of dpm_surften
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of dpm_surften
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of dpm_surften
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of dpm_surften
    """
    var_class: var_class = var_class
    """
    var_class child of dpm_surften
    """
