#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class p_sup(Group):
    """'p_sup' child."""

    fluent_name = "p-sup"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of p_sup
    """
    constant: constant = constant
    """
    constant child of p_sup
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of p_sup
    """
    field_name: field_name = field_name
    """
    field_name child of p_sup
    """
    udf: udf = udf
    """
    udf child of p_sup
    """
