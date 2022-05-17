#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .max_vol_mag import max_vol_mag
from .vol_frac_cutoff import vol_frac_cutoff
class set_velocity_and_vof_cutoffs_child(Group):
    """
    'child_object_type' of set_velocity_and_vof_cutoffs
    """

    fluent_name = "child-object-type"

    child_names = \
        ['max_vol_mag', 'vol_frac_cutoff']

    max_vol_mag: max_vol_mag = max_vol_mag
    """
    max_vol_mag child of set_velocity_and_vof_cutoffs_child
    """
    vol_frac_cutoff: vol_frac_cutoff = vol_frac_cutoff
    """
    vol_frac_cutoff child of set_velocity_and_vof_cutoffs_child
    """
