#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .display import display
from .contour_child import contour_child

class contour(NamedObject[contour_child]):
    """
    'contour' child.
    """

    fluent_name = "contour"

    command_names = \
        ['display']

    display: display = display
    """
    display command of contour
    """
    child_object_type: contour_child = contour_child
    """
    child_object_type of contour.
    """
