#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .read import read
from .replace_mesh import replace_mesh
from .write import write
from .parametric_project import parametric_project
class file(Group):
    """
    'file' child.
    """

    fluent_name = "file"

    command_names = \
        ['read', 'replace_mesh', 'write', 'parametric_project']

    read: read = read
    """
    read command of file
    """
    replace_mesh: replace_mesh = replace_mesh
    """
    replace_mesh command of file
    """
    write: write = write
    """
    write command of file
    """
    parametric_project: parametric_project = parametric_project
    """
    parametric_project command of file
    """
