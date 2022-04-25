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


class uds_diffusivity(Group):
    """'uds_diffusivity' child."""

    fluent_name = "uds-diffusivity"

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
    option child of uds_diffusivity
    """
    constant: constant = constant
    """
    constant child of uds_diffusivity
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of uds_diffusivity
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of uds_diffusivity
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of uds_diffusivity
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of uds_diffusivity
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of uds_diffusivity
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of uds_diffusivity
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of uds_diffusivity
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of uds_diffusivity
    """
    var_class: var_class = var_class
    """
    var_class child of uds_diffusivity
    """
