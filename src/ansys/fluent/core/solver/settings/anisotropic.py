#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .conductivity import conductivity
from .matrix_component import matrix_component


class anisotropic(Group):
    """'anisotropic' child."""

    fluent_name = "anisotropic"

    child_names = ["matrix_component", "conductivity"]

    matrix_component: matrix_component = matrix_component
    """
    matrix_component child of anisotropic
    """
    conductivity: conductivity = conductivity
    """
    conductivity child of anisotropic
    """
