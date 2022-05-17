#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .phase_11 import phase
from .thermal_bc import thermal_bc
from .temperature import temperature
from .q import q
class network_end_child(Group):
    """
    'child_object_type' of network_end
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'thermal_bc', 'temperature', 'q']

    phase: phase = phase
    """
    phase child of network_end_child
    """
    thermal_bc: thermal_bc = thermal_bc
    """
    thermal_bc child of network_end_child
    """
    temperature: temperature = temperature
    """
    temperature child of network_end_child
    """
    q: q = q
    """
    q child of network_end_child
    """
