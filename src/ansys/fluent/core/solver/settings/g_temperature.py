#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class g_temperature(Group):
    """'g_temperature' child."""

    fluent_name = "g-temperature"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of g_temperature
    """
    constant: constant = constant
    """
    constant child of g_temperature
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of g_temperature
    """
    field_name: field_name = field_name
    """
    field_name child of g_temperature
    """
    udf: udf = udf
    """
    udf child of g_temperature
    """
