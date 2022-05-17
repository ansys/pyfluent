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
class burn_stoichiometry(Group):
    """
    'burn_stoichiometry' child.
    """

    fluent_name = "burn-stoichiometry"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of burn_stoichiometry
    """
    constant: constant = constant
    """
    constant child of burn_stoichiometry
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of burn_stoichiometry
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of burn_stoichiometry
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of burn_stoichiometry
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of burn_stoichiometry
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of burn_stoichiometry
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of burn_stoichiometry
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of burn_stoichiometry
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of burn_stoichiometry
    """
    var_class: var_class = var_class
    """
    var_class child of burn_stoichiometry
    """
