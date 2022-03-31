#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .q import q
from .temperature import temperature
from .thermal_bc import thermal_bc


class phase_child(Group):
    """'child_object_type' of phase."""

    fluent_name = "child-object-type"

    child_names = ["thermal_bc", "temperature", "q"]

    thermal_bc: thermal_bc = thermal_bc
    """
    thermal_bc child of phase_child
    """
    temperature: temperature = temperature
    """
    temperature child of phase_child
    """
    q: q = q
    """
    q child of phase_child
    """
