#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .conductivity_0 import conductivity_0
from .conductivity_1 import conductivity_1
from .conductivity_2 import conductivity_2
from .direction_0 import direction_0
from .direction_1 import direction_1


class orthotropic(Group):
    """'orthotropic' child."""

    fluent_name = "orthotropic"

    child_names = [
        "direction_0",
        "direction_1",
        "conductivity_0",
        "conductivity_1",
        "conductivity_2",
    ]

    direction_0: direction_0 = direction_0
    """
    direction_0 child of orthotropic
    """
    direction_1: direction_1 = direction_1
    """
    direction_1 child of orthotropic
    """
    conductivity_0: conductivity_0 = conductivity_0
    """
    conductivity_0 child of orthotropic
    """
    conductivity_1: conductivity_1 = conductivity_1
    """
    conductivity_1 child of orthotropic
    """
    conductivity_2: conductivity_2 = conductivity_2
    """
    conductivity_2 child of orthotropic
    """
