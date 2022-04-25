#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class nj(Group):
    """'nj' child."""

    fluent_name = "nj"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of nj
    """
    constant: constant = constant
    """
    constant child of nj
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of nj
    """
    field_name: field_name = field_name
    """
    field_name child of nj
    """
    udf: udf = udf
    """
    udf child of nj
    """
