#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .min_value import min_value
from .max_value import max_value
class clip_to_range(Group):
    """
    'clip_to_range' child.
    """

    fluent_name = "clip-to-range"

    child_names = \
        ['min_value', 'max_value']

    min_value: min_value = min_value
    """
    min_value child of clip_to_range
    """
    max_value: max_value = max_value
    """
    max_value child of clip_to_range
    """
