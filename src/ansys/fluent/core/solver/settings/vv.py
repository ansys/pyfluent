#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class vv(Group):
    """'vv' child."""

    fluent_name = "vv"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of vv
    """
    constant: constant = constant
    """
    constant child of vv
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of vv
    """
    field_name: field_name = field_name
    """
    field_name child of vv
    """
    udf: udf = udf
    """
    udf child of vv
    """
