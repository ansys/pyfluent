#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class per_imagx(Group):
    """'per_imagx' child."""

    fluent_name = "per-imagx"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of per_imagx
    """
    constant: constant = constant
    """
    constant child of per_imagx
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of per_imagx
    """
    field_name: field_name = field_name
    """
    field_name child of per_imagx
    """
    udf: udf = udf
    """
    udf child of per_imagx
    """
