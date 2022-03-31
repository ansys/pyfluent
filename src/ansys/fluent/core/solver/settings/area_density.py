#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class area_density(Group):
    """'area_density' child."""

    fluent_name = "area-density"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of area_density
    """
    constant: constant = constant
    """
    constant child of area_density
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of area_density
    """
    field_name: field_name = field_name
    """
    field_name child of area_density
    """
    udf: udf = udf
    """
    udf child of area_density
    """
