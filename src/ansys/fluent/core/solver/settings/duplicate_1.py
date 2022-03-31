#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .design_point import design_point


class duplicate(Command):
    """Duplicate Design Point.

    Parameters
    ----------
        design_point : str
            'design_point' child.
    """

    fluent_name = "duplicate"

    argument_names = ["design_point"]

    design_point: design_point = design_point
    """
    design_point argument of duplicate
    """
