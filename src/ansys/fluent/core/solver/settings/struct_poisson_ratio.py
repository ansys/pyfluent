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


class struct_poisson_ratio(Group):
    """'struct_poisson_ratio' child."""

    fluent_name = "struct-poisson-ratio"

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
    option child of struct_poisson_ratio
    """
    constant: constant = constant
    """
    constant child of struct_poisson_ratio
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of struct_poisson_ratio
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of struct_poisson_ratio
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of struct_poisson_ratio
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of struct_poisson_ratio
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of struct_poisson_ratio
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of struct_poisson_ratio
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of struct_poisson_ratio
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of struct_poisson_ratio
    """
    var_class: var_class = var_class
    """
    var_class child of struct_poisson_ratio
    """
