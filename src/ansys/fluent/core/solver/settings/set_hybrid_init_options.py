#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .general_settings import general_settings
from .turbulent_setting import turbulent_setting


class set_hybrid_init_options(Group):
    """'set_hybrid_init_options' child."""

    fluent_name = "set-hybrid-init-options"

    child_names = ["general_settings", "turbulent_setting"]

    general_settings: general_settings = general_settings
    """
    general_settings child of set_hybrid_init_options
    """
    turbulent_setting: turbulent_setting = turbulent_setting
    """
    turbulent_setting child of set_hybrid_init_options
    """
