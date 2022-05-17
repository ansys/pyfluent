#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .feature_angle import feature_angle
class feature(Group):
    """
    'feature' child.
    """

    fluent_name = "feature"

    child_names = \
        ['feature_angle']

    feature_angle: feature_angle = feature_angle
    """
    feature_angle child of feature
    """
