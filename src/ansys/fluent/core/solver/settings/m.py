#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class m(Group):
    """'m' child."""

    fluent_name = "m"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of m
    """
    constant: constant = constant
    """
    constant child of m
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of m
    """
    field_name: field_name = field_name
    """
    field_name child of m
    """
    udf: udf = udf
    """
    udf child of m
    """
