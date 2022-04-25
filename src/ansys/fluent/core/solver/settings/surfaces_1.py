#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .plane_surface import plane_surface


class surfaces(Group):
    """'surfaces' child."""

    fluent_name = "surfaces"

    child_names = ["plane_surface"]

    plane_surface: plane_surface = plane_surface
    """
    plane_surface child of surfaces
    """
