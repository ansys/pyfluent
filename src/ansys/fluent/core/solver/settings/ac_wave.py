#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class ac_wave(Group):
    """'ac_wave' child."""

    fluent_name = "ac-wave"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of ac_wave
    """
    constant: constant = constant
    """
    constant child of ac_wave
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ac_wave
    """
    field_name: field_name = field_name
    """
    field_name child of ac_wave
    """
    udf: udf = udf
    """
    udf child of ac_wave
    """
