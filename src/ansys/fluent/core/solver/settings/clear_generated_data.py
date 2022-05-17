#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .design_points import design_points
class clear_generated_data(Command):
    """
    Clear Generated Data.
    
    Parameters
    ----------
        design_points : typing.List[str]
            'design_points' child.
    
    """

    fluent_name = "clear-generated-data"

    argument_names = \
        ['design_points']

    design_points: design_points = design_points
    """
    design_points argument of clear_generated_data
    """
