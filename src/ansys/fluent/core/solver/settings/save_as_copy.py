#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .convert_to_managed import convert_to_managed
from .project_filename import project_filename


class save_as_copy(Command):
    """Save As Project.

    Parameters
    ----------
        project_filename : str
            'project_filename' child.
        convert_to_managed : bool
            'convert_to_managed' child.
    """

    fluent_name = "save-as-copy"

    argument_names = ["project_filename", "convert_to_managed"]

    project_filename: project_filename = project_filename
    """
    project_filename argument of save_as_copy
    """
    convert_to_managed: convert_to_managed = convert_to_managed
    """
    convert_to_managed argument of save_as_copy
    """
