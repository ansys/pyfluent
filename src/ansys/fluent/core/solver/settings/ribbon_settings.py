#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .field import field
from .scalefactor import scalefactor


class ribbon_settings(Group):
    """'ribbon_settings' child."""

    fluent_name = "ribbon-settings"

    child_names = ["field", "scalefactor"]

    field: field = field
    """
    field child of ribbon_settings
    """
    scalefactor: scalefactor = scalefactor
    """
    scalefactor child of ribbon_settings
    """
