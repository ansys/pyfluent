#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class premixc(Group):
    """'premixc' child."""

    fluent_name = "premixc"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of premixc
    """
    constant: constant = constant
    """
    constant child of premixc
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of premixc
    """
    field_name: field_name = field_name
    """
    field_name child of premixc
    """
    udf: udf = udf
    """
    udf child of premixc
    """
