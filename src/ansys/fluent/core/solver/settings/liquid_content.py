#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class liquid_content(Group):
    """'liquid_content' child."""

    fluent_name = "liquid-content"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of liquid_content
    """
    constant: constant = constant
    """
    constant child of liquid_content
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of liquid_content
    """
    field_name: field_name = field_name
    """
    field_name child of liquid_content
    """
    udf: udf = udf
    """
    udf child of liquid_content
    """
