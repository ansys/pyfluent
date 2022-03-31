#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class ht_bottom(Group):
    """'ht_bottom' child."""

    fluent_name = "ht-bottom"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of ht_bottom
    """
    constant: constant = constant
    """
    constant child of ht_bottom
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ht_bottom
    """
    field_name: field_name = field_name
    """
    field_name child of ht_bottom
    """
    udf: udf = udf
    """
    udf child of ht_bottom
    """
