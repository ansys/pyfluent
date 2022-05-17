#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .residual_smoothing_factor import residual_smoothing_factor
from .residual_smoothing_iteration import residual_smoothing_iteration
class residual_smoothing(Group):
    """
    'residual_smoothing' child.
    """

    fluent_name = "residual-smoothing"

    child_names = \
        ['residual_smoothing_factor', 'residual_smoothing_iteration']

    residual_smoothing_factor: residual_smoothing_factor = residual_smoothing_factor
    """
    residual_smoothing_factor child of residual_smoothing
    """
    residual_smoothing_iteration: residual_smoothing_iteration = residual_smoothing_iteration
    """
    residual_smoothing_iteration child of residual_smoothing
    """
