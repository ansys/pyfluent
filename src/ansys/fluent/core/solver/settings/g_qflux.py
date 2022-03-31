#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class g_qflux(Group):
    """'g_qflux' child."""

    fluent_name = "g-qflux"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of g_qflux
    """
    constant: constant = constant
    """
    constant child of g_qflux
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of g_qflux
    """
    field_name: field_name = field_name
    """
    field_name child of g_qflux
    """
    udf: udf = udf
    """
    udf child of g_qflux
    """
