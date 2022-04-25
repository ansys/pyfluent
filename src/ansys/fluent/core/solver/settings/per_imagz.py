#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class per_imagz(Group):
    """'per_imagz' child."""

    fluent_name = "per-imagz"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of per_imagz
    """
    constant: constant = constant
    """
    constant child of per_imagz
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of per_imagz
    """
    field_name: field_name = field_name
    """
    field_name child of per_imagz
    """
    udf: udf = udf
    """
    udf child of per_imagz
    """
