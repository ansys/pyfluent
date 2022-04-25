#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class direction_1_z(Group):
    """'direction_1_z' child."""

    fluent_name = "direction-1-z"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of direction_1_z
    """
    constant: constant = constant
    """
    constant child of direction_1_z
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of direction_1_z
    """
    field_name: field_name = field_name
    """
    field_name child of direction_1_z
    """
    udf: udf = udf
    """
    udf child of direction_1_z
    """
