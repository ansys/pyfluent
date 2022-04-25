#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class pollut_hgo(Group):
    """'pollut_hgo' child."""

    fluent_name = "pollut-hgo"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of pollut_hgo
    """
    constant: constant = constant
    """
    constant child of pollut_hgo
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of pollut_hgo
    """
    field_name: field_name = field_name
    """
    field_name child of pollut_hgo
    """
    udf: udf = udf
    """
    udf child of pollut_hgo
    """
