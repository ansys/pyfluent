#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class direction_2_z(Group):
    """'direction_2_z' child."""

    fluent_name = "direction-2-z"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of direction_2_z
    """
    constant: constant = constant
    """
    constant child of direction_2_z
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of direction_2_z
    """
    field_name: field_name = field_name
    """
    field_name child of direction_2_z
    """
    udf: udf = udf
    """
    udf child of direction_2_z
    """
