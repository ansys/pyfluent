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


class formation_enthalpy(Group):
    """'formation_enthalpy' child."""

    fluent_name = "formation-enthalpy"

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
    option child of formation_enthalpy
    """
    constant: constant = constant
    """
    constant child of formation_enthalpy
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of formation_enthalpy
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of formation_enthalpy
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of formation_enthalpy
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of formation_enthalpy
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of formation_enthalpy
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of formation_enthalpy
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of formation_enthalpy
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of formation_enthalpy
    """
    var_class: var_class = var_class
    """
    var_class child of formation_enthalpy
    """
