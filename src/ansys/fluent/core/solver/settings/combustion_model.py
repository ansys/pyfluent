#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .boussinesq import boussinesq
from .coefficients import coefficients
from .number_of_coefficients import number_of_coefficients
from .piecewise_polynomial import piecewise_polynomial
from .nasa_9_piecewise_polynomial import nasa_9_piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .anisotropic import anisotropic
from .orthotropic import orthotropic
from .var_class import var_class
class combustion_model(Group):
    """
    'combustion_model' child.
    """

    fluent_name = "combustion-model"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of combustion_model
    """
    constant: constant = constant
    """
    constant child of combustion_model
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of combustion_model
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of combustion_model
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of combustion_model
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of combustion_model
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of combustion_model
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of combustion_model
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of combustion_model
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of combustion_model
    """
    var_class: var_class = var_class
    """
    var_class child of combustion_model
    """
