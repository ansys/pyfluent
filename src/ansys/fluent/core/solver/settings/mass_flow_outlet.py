#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .change_type import change_type
from .mass_flow_inlet_child import mass_flow_inlet_child

class mass_flow_outlet(NamedObject[mass_flow_inlet_child]):
    """
    'mass_flow_outlet' child.
    """

    fluent_name = "mass-flow-outlet"

    command_names = \
        ['change_type']

    change_type: change_type = change_type
    """
    change_type command of mass_flow_outlet
    """
    child_object_type: mass_flow_inlet_child = mass_flow_inlet_child
    """
    child_object_type of mass_flow_outlet.
    """
