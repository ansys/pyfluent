#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .factor import factor


class zoom(Command):
    """Adjust the camera field of view.

    Parameters
    ----------
        factor : real
            'factor' child.
    """

    fluent_name = "zoom"

    argument_names = ["factor"]

    factor: factor = factor
    """
    factor argument of zoom
    """
