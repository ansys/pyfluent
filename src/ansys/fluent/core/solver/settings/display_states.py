#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .copy import copy
from .display_states_child import display_states_child
from .list import list
from .read_1 import read
from .restore_state import restore_state
from .use_active import use_active
from .write_1 import write


class display_states(NamedObject[display_states_child]):
    """'display_states' child."""

    fluent_name = "display-states"

    command_names = [
        "list",
        "use_active",
        "restore_state",
        "copy",
        "read",
        "write",
    ]

    list: list = list
    """
    list command of display_states
    """
    use_active: use_active = use_active
    """
    use_active command of display_states
    """
    restore_state: restore_state = restore_state
    """
    restore_state command of display_states
    """
    copy: copy = copy
    """
    copy command of display_states
    """
    read: read = read
    """
    read command of display_states
    """
    write: write = write
    """
    write command of display_states
    """
    child_object_type: display_states_child = display_states_child
    """
    child_object_type of display_states.
    """
