#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .liquid_vof_factor import liquid_vof_factor
from .thin_film import thin_film


class boiling_parameters(Group):
    """'boiling_parameters' child."""

    fluent_name = "boiling-parameters"

    child_names = ["thin_film", "liquid_vof_factor"]

    thin_film: thin_film = thin_film
    """
    thin_film child of boiling_parameters
    """
    liquid_vof_factor: liquid_vof_factor = liquid_vof_factor
    """
    liquid_vof_factor child of boiling_parameters
    """
