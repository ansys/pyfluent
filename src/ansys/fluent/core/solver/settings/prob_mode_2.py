#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class prob_mode_2(Group):
    """'prob_mode_2' child."""

    fluent_name = "prob-mode-2"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of prob_mode_2
    """
    constant: constant = constant
    """
    constant child of prob_mode_2
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of prob_mode_2
    """
    field_name: field_name = field_name
    """
    field_name child of prob_mode_2
    """
    udf: udf = udf
    """
    udf child of prob_mode_2
    """
