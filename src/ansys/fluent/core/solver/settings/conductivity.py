#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .coefficients import coefficients
from .number_of_coefficients import number_of_coefficients
from .piecewise_linear import piecewise_linear
from .piecewise_polynomial import piecewise_polynomial
class conductivity(Group):
    """
    'conductivity' child.
    """

    fluent_name = "conductivity"

    child_names = \
        ['option', 'constant', 'coefficients', 'number_of_coefficients',
         'piecewise_linear', 'piecewise_polynomial']

    option: option = option
    """
    option child of conductivity
    """
    constant: constant = constant
    """
    constant child of conductivity
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of conductivity
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of conductivity
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of conductivity
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of conductivity
    """
