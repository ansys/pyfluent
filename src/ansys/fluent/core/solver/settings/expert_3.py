#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .mass_flux_correction_method import mass_flux_correction_method
from .hybrid_mode_selection import hybrid_mode_selection
class expert(Group):
    """
    'expert' child.
    """

    fluent_name = "expert"

    child_names = \
        ['mass_flux_correction_method', 'hybrid_mode_selection']

    mass_flux_correction_method: mass_flux_correction_method = mass_flux_correction_method
    """
    mass_flux_correction_method child of expert
    """
    hybrid_mode_selection: hybrid_mode_selection = hybrid_mode_selection
    """
    hybrid_mode_selection child of expert
    """
