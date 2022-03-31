#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .new_type import new_type
from .zone_list import zone_list


class change_type(Command):
    """'change_type' command.

    Parameters
    ----------
        zone_list : typing.List[str]
            'zone_list' child.
        new_type : str
            'new_type' child.
    """

    fluent_name = "change-type"

    argument_names = ["zone_list", "new_type"]

    zone_list: zone_list = zone_list
    """
    zone_list argument of change_type
    """
    new_type: new_type = new_type
    """
    new_type argument of change_type
    """
