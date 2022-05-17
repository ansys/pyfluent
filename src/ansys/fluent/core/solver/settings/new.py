#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .project_filename import project_filename
class new(Command):
    """
    Create New Project.
    
    Parameters
    ----------
        project_filename : str
            'project_filename' child.
    
    """

    fluent_name = "new"

    argument_names = \
        ['project_filename']

    project_filename: project_filename = project_filename
    """
    project_filename argument of new
    """
