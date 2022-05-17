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
class scattering_phase_function(Group):
    """
    'scattering_phase_function' child.
    """

    fluent_name = "scattering-phase-function"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of scattering_phase_function
    """
    constant: constant = constant
    """
    constant child of scattering_phase_function
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of scattering_phase_function
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of scattering_phase_function
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of scattering_phase_function
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of scattering_phase_function
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of scattering_phase_function
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of scattering_phase_function
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of scattering_phase_function
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of scattering_phase_function
    """
    var_class: var_class = var_class
    """
    var_class child of scattering_phase_function
    """
