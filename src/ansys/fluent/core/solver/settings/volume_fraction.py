#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class volume_fraction(Group):
    """'volume_fraction' child."""

    fluent_name = "volume-fraction"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of volume_fraction
    """
    constant: constant = constant
    """
    constant child of volume_fraction
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of volume_fraction
    """
    field_name: field_name = field_name
    """
    field_name child of volume_fraction
    """
    udf: udf = udf
    """
    udf child of volume_fraction
    """
