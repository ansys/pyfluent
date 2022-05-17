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
class lennard_jones_energy(Group):
    """
    'lennard_jones_energy' child.
    """

    fluent_name = "lennard-jones-energy"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of lennard_jones_energy
    """
    constant: constant = constant
    """
    constant child of lennard_jones_energy
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of lennard_jones_energy
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of lennard_jones_energy
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of lennard_jones_energy
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of lennard_jones_energy
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of lennard_jones_energy
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of lennard_jones_energy
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of lennard_jones_energy
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of lennard_jones_energy
    """
    var_class: var_class = var_class
    """
    var_class child of lennard_jones_energy
    """
