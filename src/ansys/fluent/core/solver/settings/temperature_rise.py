#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class temperature_rise(Group):
    """'temperature_rise' child."""

    fluent_name = "temperature-rise"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of temperature_rise
    """
    constant: constant = constant
    """
    constant child of temperature_rise
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of temperature_rise
    """
    field_name: field_name = field_name
    """
    field_name child of temperature_rise
    """
    udf: udf = udf
    """
    udf child of temperature_rise
    """
