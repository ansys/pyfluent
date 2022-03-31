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


class solid_diffusion(Group):
    """'solid_diffusion' child."""

    fluent_name = "solid-diffusion"

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
    option child of solid_diffusion
    """
    constant: constant = constant
    """
    constant child of solid_diffusion
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of solid_diffusion
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of solid_diffusion
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of solid_diffusion
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of solid_diffusion
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of solid_diffusion
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of solid_diffusion
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of solid_diffusion
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of solid_diffusion
    """
    var_class: var_class = var_class
    """
    var_class child of solid_diffusion
    """
