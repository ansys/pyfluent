#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .graphics import graphics
from .surfaces_1 import surfaces


class results(Group):
    """'results' child."""

    fluent_name = "results"

    child_names = ["graphics", "surfaces"]

    graphics: graphics = graphics
    """
    graphics child of results
    """
    surfaces: surfaces = surfaces
    """
    surfaces child of results
    """
