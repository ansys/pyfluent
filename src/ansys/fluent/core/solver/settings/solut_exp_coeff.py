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


class solut_exp_coeff(Group):
    """'solut_exp_coeff' child."""

    fluent_name = "solut-exp-coeff"

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
    option child of solut_exp_coeff
    """
    constant: constant = constant
    """
    constant child of solut_exp_coeff
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of solut_exp_coeff
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of solut_exp_coeff
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of solut_exp_coeff
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of solut_exp_coeff
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = (
        nasa_9_piecewise_polynomial
    )
    """
    nasa_9_piecewise_polynomial child of solut_exp_coeff
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of solut_exp_coeff
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of solut_exp_coeff
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of solut_exp_coeff
    """
    var_class: var_class = var_class
    """
    var_class child of solut_exp_coeff
    """
