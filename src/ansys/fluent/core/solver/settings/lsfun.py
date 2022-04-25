#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class lsfun(Group):
    """'lsfun' child."""

    fluent_name = "lsfun"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of lsfun
    """
    constant: constant = constant
    """
    constant child of lsfun
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of lsfun
    """
    field_name: field_name = field_name
    """
    field_name child of lsfun
    """
    udf: udf = udf
    """
    udf child of lsfun
    """
