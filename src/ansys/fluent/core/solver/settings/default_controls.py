#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .recommended_defaults_for_existing_cases import (
    recommended_defaults_for_existing_cases,
)
from .revert_to_pre_r20_1_default_settings import (
    revert_to_pre_r20_1_default_settings,
)


class default_controls(Group):
    """'default_controls' child."""

    fluent_name = "default-controls"

    child_names = [
        "recommended_defaults_for_existing_cases",
        "revert_to_pre_r20_1_default_settings",
    ]

    recommended_defaults_for_existing_cases: recommended_defaults_for_existing_cases = (
        recommended_defaults_for_existing_cases
    )
    """
    recommended_defaults_for_existing_cases child of default_controls
    """
    revert_to_pre_r20_1_default_settings: revert_to_pre_r20_1_default_settings = (
        revert_to_pre_r20_1_default_settings
    )
    """
    revert_to_pre_r20_1_default_settings child of default_controls
    """
