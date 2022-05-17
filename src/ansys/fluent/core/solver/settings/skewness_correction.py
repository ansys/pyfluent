#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .limit_pressure_correction_gradient import limit_pressure_correction_gradient
class skewness_correction(Group):
    """
    'skewness_correction' child.
    """

    fluent_name = "skewness-correction"

    child_names = \
        ['limit_pressure_correction_gradient']

    limit_pressure_correction_gradient: limit_pressure_correction_gradient = limit_pressure_correction_gradient
    """
    limit_pressure_correction_gradient child of skewness_correction
    """
