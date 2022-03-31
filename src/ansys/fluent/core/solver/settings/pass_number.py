#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class pass_number(Group):
    """'pass_number' child."""

    fluent_name = "pass-number"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of pass_number
    """
    constant: constant = constant
    """
    constant child of pass_number
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of pass_number
    """
    field_name: field_name = field_name
    """
    field_name child of pass_number
    """
    udf: udf = udf
    """
    udf child of pass_number
    """
