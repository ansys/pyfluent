#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .state_name import state_name
class copy(Command):
    """
    Create a new display state with settings copied from an existing display state.
    
    Parameters
    ----------
        state_name : str
            'state_name' child.
    
    """

    fluent_name = "copy"

    argument_names = \
        ['state_name']

    state_name: state_name = state_name
    """
    state_name argument of copy
    """
