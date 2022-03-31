#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .field import field
from .scalefactor import scalefactor


class ribbon(Group):
    """'ribbon' child."""

    fluent_name = "ribbon"

    child_names = ["field", "scalefactor"]

    field: field = field
    """
    field child of ribbon
    """
    scalefactor: scalefactor = scalefactor
    """
    scalefactor child of ribbon
    """
