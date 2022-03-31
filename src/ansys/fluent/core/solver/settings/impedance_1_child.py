#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .amplitude import amplitude
from .pole import pole


class impedance_1_child(Group):
    """'child_object_type' of impedance_1."""

    fluent_name = "child-object-type"

    child_names = ["pole", "amplitude"]

    pole: pole = pole
    """
    pole child of impedance_1_child
    """
    amplitude: amplitude = amplitude
    """
    amplitude child of impedance_1_child
    """
