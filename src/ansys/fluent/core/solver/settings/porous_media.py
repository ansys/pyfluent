#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .relative_permeability import relative_permeability


class porous_media(Group):
    """'porous_media' child."""

    fluent_name = "porous-media"

    child_names = ["relative_permeability"]

    relative_permeability: relative_permeability = relative_permeability
    """
    relative_permeability child of porous_media
    """
