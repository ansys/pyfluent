#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .type_1 import type
from .formula import formula
class copy_database_material_by_formula(Command):
    """
    'copy_database_material_by_formula' command.
    
    Parameters
    ----------
        type : str
            'type' child.
        formula : str
            'formula' child.
    
    """

    fluent_name = "copy-database-material-by-formula"

    argument_names = \
        ['type', 'formula']

    type: type = type
    """
    type argument of copy_database_material_by_formula
    """
    formula: formula = formula
    """
    formula argument of copy_database_material_by_formula
    """
