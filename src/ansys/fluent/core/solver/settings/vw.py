#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class vw(Group):
    """'vw' child."""

    fluent_name = "vw"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of vw
    """
    constant: constant = constant
    """
    constant child of vw
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of vw
    """
    field_name: field_name = field_name
    """
    field_name child of vw
    """
    udf: udf = udf
    """
    udf child of vw
    """
