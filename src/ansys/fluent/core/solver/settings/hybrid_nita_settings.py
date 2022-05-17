#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .multi_phase_setting import multi_phase_setting
from .single_phase_setting import single_phase_setting
class hybrid_nita_settings(Group):
    """
    'hybrid_nita_settings' child.
    """

    fluent_name = "hybrid-nita-settings"

    child_names = \
        ['multi_phase_setting', 'single_phase_setting']

    multi_phase_setting: multi_phase_setting = multi_phase_setting
    """
    multi_phase_setting child of hybrid_nita_settings
    """
    single_phase_setting: single_phase_setting = single_phase_setting
    """
    single_phase_setting child of hybrid_nita_settings
    """
