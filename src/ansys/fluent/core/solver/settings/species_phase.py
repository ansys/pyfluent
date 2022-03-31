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


class species_phase(Group):
    """'species_phase' child."""

    fluent_name = "species-phase"

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
    option child of species_phase
    """
    constant: constant = constant
    """
    constant child of species_phase
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of species_phase
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of species_phase
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of species_phase
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of species_phase
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of species_phase
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of species_phase
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of species_phase
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of species_phase
    """
    var_class: var_class = var_class
    """
    var_class child of species_phase
    """
