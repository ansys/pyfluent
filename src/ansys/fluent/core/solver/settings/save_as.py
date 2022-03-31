#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .project_filename import project_filename


class save_as(Command):
    """Save As Project.

    Parameters
    ----------
        project_filename : str
            'project_filename' child.
    """

    fluent_name = "save-as"

    argument_names = ["project_filename"]

    project_filename: project_filename = project_filename
    """
    project_filename argument of save_as
    """
