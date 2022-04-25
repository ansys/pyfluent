#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .advanced_options import advanced_options
from .formulation import formulation
from .global_time_step_settings import global_time_step_settings
from .local_time_step_settings import local_time_step_settings
from .relaxation_factors import relaxation_factors
from .verbosity_3 import verbosity


class pseudo_time_method(Group):
    """'pseudo_time_method' child."""

    fluent_name = "pseudo-time-method"

    child_names = [
        "formulation",
        "local_time_step_settings",
        "global_time_step_settings",
        "advanced_options",
        "relaxation_factors",
        "verbosity",
    ]

    formulation: formulation = formulation
    """
    formulation child of pseudo_time_method
    """
    local_time_step_settings: local_time_step_settings = (
        local_time_step_settings
    )
    """
    local_time_step_settings child of pseudo_time_method
    """
    global_time_step_settings: global_time_step_settings = (
        global_time_step_settings
    )
    """
    global_time_step_settings child of pseudo_time_method
    """
    advanced_options: advanced_options = advanced_options
    """
    advanced_options child of pseudo_time_method
    """
    relaxation_factors: relaxation_factors = relaxation_factors
    """
    relaxation_factors child of pseudo_time_method
    """
    verbosity: verbosity = verbosity
    """
    verbosity child of pseudo_time_method
    """
