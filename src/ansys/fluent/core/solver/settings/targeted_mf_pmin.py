#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class targeted_mf_pmin(Group):
    """'targeted_mf_pmin' child."""

    fluent_name = "targeted-mf-pmin"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of targeted_mf_pmin
    """
    constant: constant = constant
    """
    constant child of targeted_mf_pmin
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of targeted_mf_pmin
    """
    field_name: field_name = field_name
    """
    field_name child of targeted_mf_pmin
    """
    udf: udf = udf
    """
    udf child of targeted_mf_pmin
    """
