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


class degrees_of_freedom(Group):
    """'degrees_of_freedom' child."""

    fluent_name = "degrees-of-freedom"

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
    option child of degrees_of_freedom
    """
    constant: constant = constant
    """
    constant child of degrees_of_freedom
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of degrees_of_freedom
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of degrees_of_freedom
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of degrees_of_freedom
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of degrees_of_freedom
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of degrees_of_freedom
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of degrees_of_freedom
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of degrees_of_freedom
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of degrees_of_freedom
    """
    var_class: var_class = var_class
    """
    var_class child of degrees_of_freedom
    """
