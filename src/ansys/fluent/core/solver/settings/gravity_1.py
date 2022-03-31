#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .components import components
from .gravity import gravity


class gravity(Group):
    """'gravity' child."""

    fluent_name = "gravity"

    child_names = ["gravity", "components"]

    gravity: gravity = gravity
    """
    gravity child of gravity
    """
    components: components = components
    """
    components child of gravity
    """
