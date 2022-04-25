#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class ir_transmissivity(Group):
    """'ir_transmissivity' child."""

    fluent_name = "ir-transmissivity"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of ir_transmissivity
    """
    constant: constant = constant
    """
    constant child of ir_transmissivity
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ir_transmissivity
    """
    field_name: field_name = field_name
    """
    field_name child of ir_transmissivity
    """
    udf: udf = udf
    """
    udf child of ir_transmissivity
    """
