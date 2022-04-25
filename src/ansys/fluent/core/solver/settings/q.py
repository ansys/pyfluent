#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class q(Group):
    """'q' child."""

    fluent_name = "q"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of q
    """
    constant: constant = constant
    """
    constant child of q
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of q
    """
    field_name: field_name = field_name
    """
    field_name child of q
    """
    udf: udf = udf
    """
    udf child of q
    """
