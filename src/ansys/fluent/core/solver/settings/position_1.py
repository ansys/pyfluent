#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .xyz import xyz


class position(Command):
    """Set the camera position.

    Parameters
    ----------
        xyz : typing.List[real]
            'xyz' child.
    """

    fluent_name = "position"

    argument_names = ["xyz"]

    xyz: xyz = xyz
    """
    xyz argument of position
    """
