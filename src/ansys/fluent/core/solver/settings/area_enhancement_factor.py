#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class area_enhancement_factor(Group):
    """'area_enhancement_factor' child."""

    fluent_name = "area-enhancement-factor"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of area_enhancement_factor
    """
    constant: constant = constant
    """
    constant child of area_enhancement_factor
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of area_enhancement_factor
    """
    field_name: field_name = field_name
    """
    field_name child of area_enhancement_factor
    """
    udf: udf = udf
    """
    udf child of area_enhancement_factor
    """
