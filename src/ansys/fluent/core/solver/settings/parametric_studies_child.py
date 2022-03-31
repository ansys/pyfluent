#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .current_design_point import current_design_point
from .design_points_1 import design_points


class parametric_studies_child(Group):
    """'child_object_type' of parametric_studies."""

    fluent_name = "child-object-type"

    child_names = ["design_points", "current_design_point"]

    design_points: design_points = design_points
    """
    design_points child of parametric_studies_child
    """
    current_design_point: current_design_point = current_design_point
    """
    current_design_point child of parametric_studies_child
    """
