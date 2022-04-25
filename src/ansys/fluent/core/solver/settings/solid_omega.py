#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class solid_omega(Group):
    """'solid_omega' child."""

    fluent_name = "solid-omega"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of solid_omega
    """
    constant: constant = constant
    """
    constant child of solid_omega
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of solid_omega
    """
    field_name: field_name = field_name
    """
    field_name child of solid_omega
    """
    udf: udf = udf
    """
    udf child of solid_omega
    """
