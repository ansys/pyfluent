#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .xyz import xyz


class target(Command):
    """Set the point to be the center of the camera view.

    Parameters
    ----------
        xyz : typing.List[real]
            'xyz' child.
    """

    fluent_name = "target"

    argument_names = ["xyz"]

    xyz: xyz = xyz
    """
    xyz argument of target
    """
