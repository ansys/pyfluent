#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .coupled_vof import coupled_vof
from .rhie_chow_flux import rhie_chow_flux
from .skewness_correction import skewness_correction
class p_v_coupling(Group):
    """
    'p_v_coupling' child.
    """

    fluent_name = "p-v-coupling"

    child_names = \
        ['coupled_vof', 'rhie_chow_flux', 'skewness_correction']

    coupled_vof: coupled_vof = coupled_vof
    """
    coupled_vof child of p_v_coupling
    """
    rhie_chow_flux: rhie_chow_flux = rhie_chow_flux
    """
    rhie_chow_flux child of p_v_coupling
    """
    skewness_correction: skewness_correction = skewness_correction
    """
    skewness_correction child of p_v_coupling
    """
