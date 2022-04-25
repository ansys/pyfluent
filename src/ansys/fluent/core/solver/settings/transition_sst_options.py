#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .roughness_correlation import roughness_correlation


class transition_sst_options(Group):
    """'transition_sst_options' child."""

    fluent_name = "transition-sst-options"

    child_names = ["roughness_correlation"]

    roughness_correlation: roughness_correlation = roughness_correlation
    """
    roughness_correlation child of transition_sst_options
    """
