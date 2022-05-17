#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .filepath import filepath
from .delete_existing import delete_existing
class import_design_table(Command):
    """
    Import Design Point Table.
    
    Parameters
    ----------
        filepath : str
            'filepath' child.
        delete_existing : bool
            'delete_existing' child.
    
    """

    fluent_name = "import-design-table"

    argument_names = \
        ['filepath', 'delete_existing']

    filepath: filepath = filepath
    """
    filepath argument of import_design_table
    """
    delete_existing: delete_existing = delete_existing
    """
    delete_existing argument of import_design_table
    """
