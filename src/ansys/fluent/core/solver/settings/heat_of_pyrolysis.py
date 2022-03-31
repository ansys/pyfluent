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


class heat_of_pyrolysis(Group):
    """'heat_of_pyrolysis' child."""

    fluent_name = "heat-of-pyrolysis"

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
    option child of heat_of_pyrolysis
    """
    constant: constant = constant
    """
    constant child of heat_of_pyrolysis
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of heat_of_pyrolysis
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of heat_of_pyrolysis
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of heat_of_pyrolysis
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of heat_of_pyrolysis
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of heat_of_pyrolysis
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of heat_of_pyrolysis
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of heat_of_pyrolysis
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of heat_of_pyrolysis
    """
    var_class: var_class = var_class
    """
    var_class child of heat_of_pyrolysis
    """
