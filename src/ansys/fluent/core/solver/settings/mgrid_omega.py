#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class mgrid_omega(Group):
    """'mgrid_omega' child."""

    fluent_name = "mgrid-omega"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of mgrid_omega
    """
    constant: constant = constant
    """
    constant child of mgrid_omega
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of mgrid_omega
    """
    field_name: field_name = field_name
    """
    field_name child of mgrid_omega
    """
    udf: udf = udf
    """
    udf child of mgrid_omega
    """
