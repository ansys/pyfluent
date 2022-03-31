#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class t0(Group):
    """'t0' child."""

    fluent_name = "t0"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of t0
    """
    constant: constant = constant
    """
    constant child of t0
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of t0
    """
    field_name: field_name = field_name
    """
    field_name child of t0
    """
    udf: udf = udf
    """
    udf child of t0
    """
