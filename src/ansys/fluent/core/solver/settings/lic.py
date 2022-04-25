#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .display import display
from .lic_child import lic_child


class lic(NamedObject[lic_child]):
    """'lic' child."""

    fluent_name = "lic"

    command_names = ["display"]

    display: display = display
    """
    display command of lic
    """
    child_object_type: lic_child = lic_child
    """
    child_object_type of lic.
    """
