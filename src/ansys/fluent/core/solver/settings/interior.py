#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .interior_child import interior_child

class interior(NamedObject[interior_child]):
    """
    'interior' child.
    """

    fluent_name = "interior"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of interior
    """
    child_object_type: interior_child = interior_child
    """
    child_object_type of interior.
    """
