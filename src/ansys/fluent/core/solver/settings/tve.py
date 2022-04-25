#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class tve(Group):
    """'tve' child."""

    fluent_name = "tve"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of tve
    """
    constant: constant = constant
    """
    constant child of tve
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of tve
    """
    field_name: field_name = field_name
    """
    field_name child of tve
    """
    udf: udf = udf
    """
    udf child of tve
    """
