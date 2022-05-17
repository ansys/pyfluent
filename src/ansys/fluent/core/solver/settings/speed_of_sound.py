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
class speed_of_sound(Group):
    """
    'speed_of_sound' child.
    """

    fluent_name = "speed-of-sound"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of speed_of_sound
    """
    constant: constant = constant
    """
    constant child of speed_of_sound
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of speed_of_sound
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of speed_of_sound
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of speed_of_sound
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of speed_of_sound
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of speed_of_sound
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of speed_of_sound
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of speed_of_sound
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of speed_of_sound
    """
    var_class: var_class = var_class
    """
    var_class child of speed_of_sound
    """
