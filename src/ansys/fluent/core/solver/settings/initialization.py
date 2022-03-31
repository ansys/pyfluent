#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .dpm_reset import dpm_reset
from .fmg_initialize import fmg_initialize
from .fmg_options import fmg_options
from .hybrid_initialize import hybrid_initialize
from .init_acoustics_options import init_acoustics_options
from .init_flow_statistics import init_flow_statistics
from .localized_turb_init import localized_turb_init
from .lwf_reset import lwf_reset
from .patch import patch
from .reference_frame_1 import reference_frame
from .set_hybrid_init_options import set_hybrid_init_options
from .standard_initialize import standard_initialize


class initialization(Group):
    """'initialization' child."""

    fluent_name = "initialization"

    child_names = [
        "fmg_initialize",
        "localized_turb_init",
        "reference_frame",
        "fmg_options",
        "set_hybrid_init_options",
        "patch",
    ]

    fmg_initialize: fmg_initialize = fmg_initialize
    """
    fmg_initialize child of initialization
    """
    localized_turb_init: localized_turb_init = localized_turb_init
    """
    localized_turb_init child of initialization
    """
    reference_frame: reference_frame = reference_frame
    """
    reference_frame child of initialization
    """
    fmg_options: fmg_options = fmg_options
    """
    fmg_options child of initialization
    """
    set_hybrid_init_options: set_hybrid_init_options = set_hybrid_init_options
    """
    set_hybrid_init_options child of initialization
    """
    patch: patch = patch
    """
    patch child of initialization
    """
    command_names = [
        "standard_initialize",
        "hybrid_initialize",
        "dpm_reset",
        "lwf_reset",
        "init_flow_statistics",
        "init_acoustics_options",
    ]

    standard_initialize: standard_initialize = standard_initialize
    """
    standard_initialize command of initialization
    """
    hybrid_initialize: hybrid_initialize = hybrid_initialize
    """
    hybrid_initialize command of initialization
    """
    dpm_reset: dpm_reset = dpm_reset
    """
    dpm_reset command of initialization
    """
    lwf_reset: lwf_reset = lwf_reset
    """
    lwf_reset command of initialization
    """
    init_flow_statistics: init_flow_statistics = init_flow_statistics
    """
    init_flow_statistics command of initialization
    """
    init_acoustics_options: init_acoustics_options = init_acoustics_options
    """
    init_acoustics_options command of initialization
    """
