#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .automatic import automatic
from .manual import manual
from .option import option


class coloring(Group):
    """'coloring' child."""

    fluent_name = "coloring"

    child_names = ["option", "automatic", "manual"]

    option: option = option
    """
    option child of coloring
    """
    automatic: automatic = automatic
    """
    automatic child of coloring
    """
    manual: manual = manual
    """
    manual child of coloring
    """
