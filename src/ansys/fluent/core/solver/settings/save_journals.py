#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .separate_journals import separate_journals


class save_journals(Command):
    """Save Journals.

    Parameters
    ----------
        separate_journals : bool
            'separate_journals' child.
    """

    fluent_name = "save-journals"

    argument_names = ["separate_journals"]

    separate_journals: separate_journals = separate_journals
    """
    separate_journals argument of save_journals
    """
