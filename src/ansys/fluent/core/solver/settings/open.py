#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .project_filename import project_filename
from .load_case import load_case
class open(Command):
    """
    Open project.
    
    Parameters
    ----------
        project_filename : str
            'project_filename' child.
        load_case : bool
            'load_case' child.
    
    """

    fluent_name = "open"

    argument_names = \
        ['project_filename', 'load_case']

    project_filename: project_filename = project_filename
    """
    project_filename argument of open
    """
    load_case: load_case = load_case
    """
    load_case argument of open
    """
