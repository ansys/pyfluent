#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .file_name import file_name
from .state_name_1 import state_name


class write(Command):
    """Write display states to a file.

    Parameters
    ----------
        file_name : str
            'file_name' child.
        state_name : typing.List[str]
            'state_name' child.
    """

    fluent_name = "write"

    argument_names = ["file_name", "state_name"]

    file_name: file_name = file_name
    """
    file_name argument of write
    """
    state_name: state_name = state_name
    """
    state_name argument of write
    """
