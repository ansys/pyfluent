#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class caf(Group):
    """'caf' child."""

    fluent_name = "caf"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of caf
    """
    constant: constant = constant
    """
    constant child of caf
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of caf
    """
    field_name: field_name = field_name
    """
    field_name child of caf
    """
    udf: udf = udf
    """
    udf child of caf
    """
