#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class uu(Group):
    """'uu' child."""

    fluent_name = "uu"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of uu
    """
    constant: constant = constant
    """
    constant child of uu
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of uu
    """
    field_name: field_name = field_name
    """
    field_name child of uu
    """
    udf: udf = udf
    """
    udf child of uu
    """
