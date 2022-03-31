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


class species(Group):
    """'species' child."""

    fluent_name = "species"

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
    option child of species
    """
    constant: constant = constant
    """
    constant child of species
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of species
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of species
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of species
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of species
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of species
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of species
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of species
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of species
    """
    var_class: var_class = var_class
    """
    var_class child of species
    """
