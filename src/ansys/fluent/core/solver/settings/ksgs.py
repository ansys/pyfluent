#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class ksgs(Group):
    """'ksgs' child."""

    fluent_name = "ksgs"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of ksgs
    """
    constant: constant = constant
    """
    constant child of ksgs
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ksgs
    """
    field_name: field_name = field_name
    """
    field_name child of ksgs
    """
    udf: udf = udf
    """
    udf child of ksgs
    """
