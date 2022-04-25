#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class h(Group):
    """'h' child."""

    fluent_name = "h"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of h
    """
    constant: constant = constant
    """
    constant child of h
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of h
    """
    field_name: field_name = field_name
    """
    field_name child of h
    """
    udf: udf = udf
    """
    udf child of h
    """
