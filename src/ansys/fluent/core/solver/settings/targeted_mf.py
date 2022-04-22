#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class targeted_mf(Group):
    """'targeted_mf' child."""

    fluent_name = "targeted-mf"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of targeted_mf
    """
    constant: constant = constant
    """
    constant child of targeted_mf
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of targeted_mf
    """
    field_name: field_name = field_name
    """
    field_name child of targeted_mf
    """
    udf: udf = udf
    """
    udf child of targeted_mf
    """
