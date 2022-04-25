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


class premix_unburnt_fuel_mf(Group):
    """'premix_unburnt_fuel_mf' child."""

    fluent_name = "premix-unburnt-fuel-mf"

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
    option child of premix_unburnt_fuel_mf
    """
    constant: constant = constant
    """
    constant child of premix_unburnt_fuel_mf
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of premix_unburnt_fuel_mf
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of premix_unburnt_fuel_mf
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of premix_unburnt_fuel_mf
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of premix_unburnt_fuel_mf
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of premix_unburnt_fuel_mf
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of premix_unburnt_fuel_mf
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of premix_unburnt_fuel_mf
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of premix_unburnt_fuel_mf
    """
    var_class: var_class = var_class
    """
    var_class child of premix_unburnt_fuel_mf
    """
