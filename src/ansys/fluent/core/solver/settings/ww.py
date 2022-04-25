#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class ww(Group):
    """'ww' child."""

    fluent_name = "ww"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of ww
    """
    constant: constant = constant
    """
    constant child of ww
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ww
    """
    field_name: field_name = field_name
    """
    field_name child of ww
    """
    udf: udf = udf
    """
    udf child of ww
    """
