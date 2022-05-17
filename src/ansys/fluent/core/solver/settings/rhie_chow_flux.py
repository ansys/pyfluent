#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .low_order_rhie_chow import low_order_rhie_chow
class rhie_chow_flux(Group):
    """
    'rhie_chow_flux' child.
    """

    fluent_name = "rhie-chow-flux"

    child_names = \
        ['low_order_rhie_chow']

    low_order_rhie_chow: low_order_rhie_chow = low_order_rhie_chow
    """
    low_order_rhie_chow child of rhie_chow_flux
    """
