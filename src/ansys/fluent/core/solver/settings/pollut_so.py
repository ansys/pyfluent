#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class pollut_so(Group):
    """'pollut_so' child."""

    fluent_name = "pollut-so"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of pollut_so
    """
    constant: constant = constant
    """
    constant child of pollut_so
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of pollut_so
    """
    field_name: field_name = field_name
    """
    field_name child of pollut_so
    """
    udf: udf = udf
    """
    udf child of pollut_so
    """
