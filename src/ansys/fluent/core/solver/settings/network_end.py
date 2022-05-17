#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .network_end_child import network_end_child

class network_end(NamedObject[network_end_child]):
    """
    'network_end' child.
    """

    fluent_name = "network-end"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of network_end
    """
    child_object_type: network_end_child = network_end_child
    """
    child_object_type of network_end.
    """
