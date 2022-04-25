#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class amp(Group):
    """'amp' child."""

    fluent_name = "amp"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of amp
    """
    constant: constant = constant
    """
    constant child of amp
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of amp
    """
    field_name: field_name = field_name
    """
    field_name child of amp
    """
    udf: udf = udf
    """
    udf child of amp
    """
