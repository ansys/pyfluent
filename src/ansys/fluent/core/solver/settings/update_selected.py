#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .design_points import design_points


class update_selected(Command):
    """Update Selected Design Points.

    Parameters
    ----------
        design_points : typing.List[str]
            'design_points' child.
    """

    fluent_name = "update-selected"

    argument_names = ["design_points"]

    design_points: design_points = design_points
    """
    design_points argument of update_selected
    """
