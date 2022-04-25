#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .algebric_mg_controls import algebric_mg_controls
from .amg_gpgpu_options import amg_gpgpu_options
from .fas_mg_controls import fas_mg_controls
from .multi_grid_controls import multi_grid_controls


class multi_grid(Group):
    """'multi_grid' child."""

    fluent_name = "multi-grid"

    child_names = [
        "multi_grid_controls",
        "algebric_mg_controls",
        "fas_mg_controls",
        "amg_gpgpu_options",
    ]

    multi_grid_controls: multi_grid_controls = multi_grid_controls
    """
    multi_grid_controls child of multi_grid
    """
    algebric_mg_controls: algebric_mg_controls = algebric_mg_controls
    """
    algebric_mg_controls child of multi_grid
    """
    fas_mg_controls: fas_mg_controls = fas_mg_controls
    """
    fas_mg_controls child of multi_grid
    """
    amg_gpgpu_options: amg_gpgpu_options = amg_gpgpu_options
    """
    amg_gpgpu_options child of multi_grid
    """
