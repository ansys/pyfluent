#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .state_name import state_name


class restore_state(Command):
    """Apply a display state to the active window.

    Parameters
    ----------
        state_name : str
            'state_name' child.
    """

    fluent_name = "restore-state"

    argument_names = ["state_name"]

    state_name: state_name = state_name
    """
    state_name argument of restore_state
    """
