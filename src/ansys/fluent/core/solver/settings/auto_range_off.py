#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .clip_to_range import clip_to_range
from .minimum import minimum
from .maximum import maximum
class auto_range_off(Group):
    """
    'auto_range_off' child.
    """

    fluent_name = "auto-range-off"

    child_names = \
        ['clip_to_range', 'minimum', 'maximum']

    clip_to_range: clip_to_range = clip_to_range
    """
    clip_to_range child of auto_range_off
    """
    minimum: minimum = minimum
    """
    minimum child of auto_range_off
    """
    maximum: maximum = maximum
    """
    maximum child of auto_range_off
    """
