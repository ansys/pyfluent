#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .number_of_iterations import number_of_iterations
from .explicit_urf import explicit_urf
from .reference_frame_1 import reference_frame
from .initial_pressure import initial_pressure
from .external_aero import external_aero
from .const_velocity import const_velocity
class general_settings(Group):
    """
    Enter the general settings menu.
    """

    fluent_name = "general-settings"

    child_names = \
        ['number_of_iterations', 'explicit_urf', 'reference_frame',
         'initial_pressure', 'external_aero', 'const_velocity']

    number_of_iterations: number_of_iterations = number_of_iterations
    """
    number_of_iterations child of general_settings
    """
    explicit_urf: explicit_urf = explicit_urf
    """
    explicit_urf child of general_settings
    """
    reference_frame: reference_frame = reference_frame
    """
    reference_frame child of general_settings
    """
    initial_pressure: initial_pressure = initial_pressure
    """
    initial_pressure child of general_settings
    """
    external_aero: external_aero = external_aero
    """
    external_aero child of general_settings
    """
    const_velocity: const_velocity = const_velocity
    """
    const_velocity child of general_settings
    """
