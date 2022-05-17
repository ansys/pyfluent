#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .pressure_velocity_coupling_controls import pressure_velocity_coupling_controls
from .pressure_velocity_coupling_method import pressure_velocity_coupling_method
from .gradient_controls import gradient_controls
from .specify_gradient_method import specify_gradient_method
class methods(Group):
    """
    'methods' child.
    """

    fluent_name = "methods"

    child_names = \
        ['pressure_velocity_coupling_controls',
         'pressure_velocity_coupling_method', 'gradient_controls',
         'specify_gradient_method']

    pressure_velocity_coupling_controls: pressure_velocity_coupling_controls = pressure_velocity_coupling_controls
    """
    pressure_velocity_coupling_controls child of methods
    """
    pressure_velocity_coupling_method: pressure_velocity_coupling_method = pressure_velocity_coupling_method
    """
    pressure_velocity_coupling_method child of methods
    """
    gradient_controls: gradient_controls = gradient_controls
    """
    gradient_controls child of methods
    """
    specify_gradient_method: specify_gradient_method = specify_gradient_method
    """
    specify_gradient_method child of methods
    """
