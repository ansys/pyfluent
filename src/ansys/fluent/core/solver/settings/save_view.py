#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .view_name import view_name


class save_view(Command):
    """Save the current view to the view list.

    Parameters
    ----------
        view_name : str
            'view_name' child.
    """

    fluent_name = "save-view"

    argument_names = ["view_name"]

    view_name: view_name = view_name
    """
    view_name argument of save_view
    """
