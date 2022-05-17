#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .network_child import network_child

class network(NamedObject[network_child]):
    """
    'network' child.
    """

    fluent_name = "network"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of network
    """
    child_object_type: network_child = network_child
    """
    child_object_type of network.
    """
