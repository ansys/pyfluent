#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .file_name import file_name


class read(Command):
    """Read display states from a file.

    Parameters
    ----------
        file_name : str
            'file_name' child.
    """

    fluent_name = "read"

    argument_names = ["file_name"]

    file_name: file_name = file_name
    """
    file_name argument of read
    """
