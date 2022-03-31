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


class scattering_factor(Group):
    """'scattering_factor' child."""

    fluent_name = "scattering-factor"

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
    option child of scattering_factor
    """
    constant: constant = constant
    """
    constant child of scattering_factor
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of scattering_factor
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of scattering_factor
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of scattering_factor
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of scattering_factor
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of scattering_factor
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of scattering_factor
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of scattering_factor
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of scattering_factor
    """
    var_class: var_class = var_class
    """
    var_class child of scattering_factor
    """
