#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .radiator_child import radiator_child

class radiator(NamedObject[radiator_child]):
    """
    'radiator' child.
    """

    fluent_name = "radiator"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of radiator
    """
    child_object_type: radiator_child = radiator_child
    """
    child_object_type of radiator.
    """
