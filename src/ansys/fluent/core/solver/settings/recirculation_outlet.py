#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .recirculation_outlet_child import recirculation_outlet_child

class recirculation_outlet(NamedObject[recirculation_outlet_child]):
    """
    'recirculation_outlet' child.
    """

    fluent_name = "recirculation-outlet"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of recirculation_outlet
    """
    child_object_type: recirculation_outlet_child = recirculation_outlet_child
    """
    child_object_type of recirculation_outlet.
    """
