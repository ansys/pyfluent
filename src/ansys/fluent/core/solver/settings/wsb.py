#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class wsb(Group):
    """'wsb' child."""

    fluent_name = "wsb"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of wsb
    """
    constant: constant = constant
    """
    constant child of wsb
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of wsb
    """
    field_name: field_name = field_name
    """
    field_name child of wsb
    """
    udf: udf = udf
    """
    udf child of wsb
    """
