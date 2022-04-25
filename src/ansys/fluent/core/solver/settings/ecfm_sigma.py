#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class ecfm_sigma(Group):
    """'ecfm_sigma' child."""

    fluent_name = "ecfm-sigma"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of ecfm_sigma
    """
    constant: constant = constant
    """
    constant child of ecfm_sigma
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ecfm_sigma
    """
    field_name: field_name = field_name
    """
    field_name child of ecfm_sigma
    """
    udf: udf = udf
    """
    udf child of ecfm_sigma
    """
