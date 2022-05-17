#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .design_points import design_points
class delete_design_points(Command):
    """
    Delete Design Points.
    
    Parameters
    ----------
        design_points : typing.List[str]
            'design_points' child.
    
    """

    fluent_name = "delete-design-points"

    argument_names = \
        ['design_points']

    design_points: design_points = design_points
    """
    design_points argument of delete_design_points
    """
