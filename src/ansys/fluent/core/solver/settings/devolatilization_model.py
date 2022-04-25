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


class devolatilization_model(Group):
    """'devolatilization_model' child."""

    fluent_name = "devolatilization-model"

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
    option child of devolatilization_model
    """
    constant: constant = constant
    """
    constant child of devolatilization_model
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of devolatilization_model
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of devolatilization_model
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of devolatilization_model
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of devolatilization_model
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of devolatilization_model
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of devolatilization_model
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of devolatilization_model
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of devolatilization_model
    """
    var_class: var_class = var_class
    """
    var_class child of devolatilization_model
    """
