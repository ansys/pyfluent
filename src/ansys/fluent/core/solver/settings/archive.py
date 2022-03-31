#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .archive_name import archive_name


class archive(Command):
    """Archive Project.

    Parameters
    ----------
        archive_name : str
            'archive_name' child.
    """

    fluent_name = "archive"

    argument_names = ["archive_name"]

    archive_name: archive_name = archive_name
    """
    archive_name argument of archive
    """
