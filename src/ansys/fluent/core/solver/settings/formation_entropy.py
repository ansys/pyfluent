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


class formation_entropy(Group):
    """'formation_entropy' child."""

    fluent_name = "formation-entropy"

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
    option child of formation_entropy
    """
    constant: constant = constant
    """
    constant child of formation_entropy
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of formation_entropy
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of formation_entropy
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of formation_entropy
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of formation_entropy
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of formation_entropy
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of formation_entropy
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of formation_entropy
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of formation_entropy
    """
    var_class: var_class = var_class
    """
    var_class child of formation_entropy
    """
