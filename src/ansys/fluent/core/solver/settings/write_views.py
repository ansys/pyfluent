#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .file_name import file_name
from .view_list import view_list


class write_views(Command):
    """Write selected views to a view file.

    Parameters
    ----------
        file_name : str
            'file_name' child.
        view_list : typing.List[str]
            'view_list' child.
    """

    fluent_name = "write-views"

    argument_names = ["file_name", "view_list"]

    file_name: file_name = file_name
    """
    file_name argument of write_views
    """
    view_list: view_list = view_list
    """
    view_list argument of write_views
    """
