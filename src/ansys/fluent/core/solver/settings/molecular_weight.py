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


class molecular_weight(Group):
    """'molecular_weight' child."""

    fluent_name = "molecular-weight"

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
    option child of molecular_weight
    """
    constant: constant = constant
    """
    constant child of molecular_weight
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of molecular_weight
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of molecular_weight
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of molecular_weight
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of molecular_weight
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of molecular_weight
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of molecular_weight
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of molecular_weight
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of molecular_weight
    """
    var_class: var_class = var_class
    """
    var_class child of molecular_weight
    """
