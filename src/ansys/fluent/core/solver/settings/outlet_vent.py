#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .outlet_vent_child import outlet_vent_child

class outlet_vent(NamedObject[outlet_vent_child]):
    """
    'outlet_vent' child.
    """

    fluent_name = "outlet-vent"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of outlet_vent
    """
    child_object_type: outlet_vent_child = outlet_vent_child
    """
    child_object_type of outlet_vent.
    """
