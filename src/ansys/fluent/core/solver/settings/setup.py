#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .boundary_conditions import boundary_conditions
from .cell_zone_conditions import cell_zone_conditions
from .general import general
from .materials import materials
from .models_1 import models
from .reference_values import reference_values


class setup(Group):
    """'setup' child."""

    fluent_name = "setup"

    child_names = [
        "general",
        "models",
        "materials",
        "cell_zone_conditions",
        "boundary_conditions",
        "reference_values",
    ]

    general: general = general
    """
    general child of setup
    """
    models: models = models
    """
    models child of setup
    """
    materials: materials = materials
    """
    materials child of setup
    """
    cell_zone_conditions: cell_zone_conditions = cell_zone_conditions
    """
    cell_zone_conditions child of setup
    """
    boundary_conditions: boundary_conditions = boundary_conditions
    """
    boundary_conditions child of setup
    """
    reference_values: reference_values = reference_values
    """
    reference_values child of setup
    """
