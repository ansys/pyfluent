#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .averaged_turbulent_parameters import averaged_turbulent_parameters
from .turbulent_intensity_1 import turbulent_intensity
from .viscosity_ratio_1 import viscosity_ratio
class turbulent_setting(Group):
    """
    Enter the turbulent settings menu.
    """

    fluent_name = "turbulent-setting"

    child_names = \
        ['averaged_turbulent_parameters', 'turbulent_intensity',
         'viscosity_ratio']

    averaged_turbulent_parameters: averaged_turbulent_parameters = averaged_turbulent_parameters
    """
    averaged_turbulent_parameters child of turbulent_setting
    """
    turbulent_intensity: turbulent_intensity = turbulent_intensity
    """
    turbulent_intensity child of turbulent_setting
    """
    viscosity_ratio: viscosity_ratio = viscosity_ratio
    """
    viscosity_ratio child of turbulent_setting
    """
