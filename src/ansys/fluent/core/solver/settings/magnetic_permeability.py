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


class magnetic_permeability(Group):
    """'magnetic_permeability' child."""

    fluent_name = "magnetic-permeability"

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
    option child of magnetic_permeability
    """
    constant: constant = constant
    """
    constant child of magnetic_permeability
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of magnetic_permeability
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of magnetic_permeability
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of magnetic_permeability
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of magnetic_permeability
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of magnetic_permeability
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of magnetic_permeability
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of magnetic_permeability
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of magnetic_permeability
    """
    var_class: var_class = var_class
    """
    var_class child of magnetic_permeability
    """
