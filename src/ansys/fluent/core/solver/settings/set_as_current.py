#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .study_name import study_name
class set_as_current(Command):
    """
    Set As Current Study.
    
    Parameters
    ----------
        study_name : str
            'study_name' child.
    
    """

    fluent_name = "set-as-current"

    argument_names = \
        ['study_name']

    study_name: study_name = study_name
    """
    study_name argument of set_as_current
    """
