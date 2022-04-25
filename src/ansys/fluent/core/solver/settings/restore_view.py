#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .view_name import view_name


class restore_view(Command):
    """Use a saved view.

    Parameters
    ----------
        view_name : str
            'view_name' child.
    """

    fluent_name = "restore-view"

    argument_names = ["view_name"]

    view_name: view_name = view_name
    """
    view_name argument of restore_view
    """
