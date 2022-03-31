#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .execute_smoothing import execute_smoothing
from .patch_reconstructed_interface import patch_reconstructed_interface
from .smoothing_relaxation_factor import smoothing_relaxation_factor
from .use_volumetric_smoothing import use_volumetric_smoothing


class vof_smooth_options(Group):
    """'vof_smooth_options' child."""

    fluent_name = "vof-smooth-options"

    child_names = [
        "patch_reconstructed_interface",
        "use_volumetric_smoothing",
        "smoothing_relaxation_factor",
    ]

    patch_reconstructed_interface: patch_reconstructed_interface = (
        patch_reconstructed_interface
    )
    """
    patch_reconstructed_interface child of vof_smooth_options
    """
    use_volumetric_smoothing: use_volumetric_smoothing = (
        use_volumetric_smoothing
    )
    """
    use_volumetric_smoothing child of vof_smooth_options
    """
    smoothing_relaxation_factor: smoothing_relaxation_factor = (
        smoothing_relaxation_factor
    )
    """
    smoothing_relaxation_factor child of vof_smooth_options
    """
    command_names = ["execute_smoothing"]

    execute_smoothing: execute_smoothing = execute_smoothing
    """
    execute_smoothing command of vof_smooth_options
    """
