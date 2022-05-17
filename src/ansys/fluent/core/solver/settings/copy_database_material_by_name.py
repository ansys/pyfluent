#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .type_1 import type
from .name import name
class copy_database_material_by_name(Command):
    """
    'copy_database_material_by_name' command.
    
    Parameters
    ----------
        type : str
            'type' child.
        name : str
            'name' child.
    
    """

    fluent_name = "copy-database-material-by-name"

    argument_names = \
        ['type', 'name']

    type: type = type
    """
    type argument of copy_database_material_by_name
    """
    name: name = name
    """
    name argument of copy_database_material_by_name
    """
