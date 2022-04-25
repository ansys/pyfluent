#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .kw_low_re_correction import kw_low_re_correction
from .kw_shear_correction import kw_shear_correction
from .turb_compressibility import turb_compressibility


class k_omega_options(Group):
    """'k_omega_options' child."""

    fluent_name = "k-omega-options"

    child_names = [
        "kw_low_re_correction",
        "kw_shear_correction",
        "turb_compressibility",
    ]

    kw_low_re_correction: kw_low_re_correction = kw_low_re_correction
    """
    kw_low_re_correction child of k_omega_options
    """
    kw_shear_correction: kw_shear_correction = kw_shear_correction
    """
    kw_shear_correction child of k_omega_options
    """
    turb_compressibility: turb_compressibility = turb_compressibility
    """
    turb_compressibility child of k_omega_options
    """
