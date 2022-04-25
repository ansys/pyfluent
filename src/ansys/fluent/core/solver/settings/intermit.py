#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class intermit(Group):
    """'intermit' child."""

    fluent_name = "intermit"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of intermit
    """
    constant: constant = constant
    """
    constant child of intermit
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of intermit
    """
    field_name: field_name = field_name
    """
    field_name child of intermit
    """
    udf: udf = udf
    """
    udf child of intermit
    """
