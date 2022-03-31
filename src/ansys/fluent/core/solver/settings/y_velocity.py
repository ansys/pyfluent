#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class y_velocity(Group):
    """'y_velocity' child."""

    fluent_name = "y-velocity"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of y_velocity
    """
    constant: constant = constant
    """
    constant child of y_velocity
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of y_velocity
    """
    field_name: field_name = field_name
    """
    field_name child of y_velocity
    """
    udf: udf = udf
    """
    udf child of y_velocity
    """
