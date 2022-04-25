#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class v_absp(Group):
    """'v_absp' child."""

    fluent_name = "v-absp"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of v_absp
    """
    constant: constant = constant
    """
    constant child of v_absp
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of v_absp
    """
    field_name: field_name = field_name
    """
    field_name child of v_absp
    """
    udf: udf = udf
    """
    udf child of v_absp
    """
