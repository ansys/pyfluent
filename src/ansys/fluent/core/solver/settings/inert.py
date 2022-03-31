#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class inert(Group):
    """'inert' child."""

    fluent_name = "inert"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of inert
    """
    constant: constant = constant
    """
    constant child of inert
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of inert
    """
    field_name: field_name = field_name
    """
    field_name child of inert
    """
    udf: udf = udf
    """
    udf child of inert
    """
