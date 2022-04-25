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


class reaction_mechs(Group):
    """'reaction_mechs' child."""

    fluent_name = "reaction-mechs"

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
    option child of reaction_mechs
    """
    constant: constant = constant
    """
    constant child of reaction_mechs
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of reaction_mechs
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of reaction_mechs
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of reaction_mechs
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of reaction_mechs
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of reaction_mechs
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of reaction_mechs
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of reaction_mechs
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of reaction_mechs
    """
    var_class: var_class = var_class
    """
    var_class child of reaction_mechs
    """
