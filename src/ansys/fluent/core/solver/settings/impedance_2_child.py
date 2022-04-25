#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .amplitude_imag import amplitude_imag
from .amplitude_real import amplitude_real
from .pole_imag import pole_imag
from .pole_real import pole_real


class impedance_2_child(Group):
    """'child_object_type' of impedance_2."""

    fluent_name = "child-object-type"

    child_names = [
        "pole_real",
        "pole_imag",
        "amplitude_real",
        "amplitude_imag",
    ]

    pole_real: pole_real = pole_real
    """
    pole_real child of impedance_2_child
    """
    pole_imag: pole_imag = pole_imag
    """
    pole_imag child of impedance_2_child
    """
    amplitude_real: amplitude_real = amplitude_real
    """
    amplitude_real child of impedance_2_child
    """
    amplitude_imag: amplitude_imag = amplitude_imag
    """
    amplitude_imag child of impedance_2_child
    """
