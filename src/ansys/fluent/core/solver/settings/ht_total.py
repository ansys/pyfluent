#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class ht_total(Group):
    """'ht_total' child."""

    fluent_name = "ht-total"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of ht_total
    """
    constant: constant = constant
    """
    constant child of ht_total
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ht_total
    """
    field_name: field_name = field_name
    """
    field_name child of ht_total
    """
    udf: udf = udf
    """
    udf child of ht_total
    """
