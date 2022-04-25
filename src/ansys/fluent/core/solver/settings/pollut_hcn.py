#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class pollut_hcn(Group):
    """'pollut_hcn' child."""

    fluent_name = "pollut-hcn"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of pollut_hcn
    """
    constant: constant = constant
    """
    constant child of pollut_hcn
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of pollut_hcn
    """
    field_name: field_name = field_name
    """
    field_name child of pollut_hcn
    """
    udf: udf = udf
    """
    udf child of pollut_hcn
    """
