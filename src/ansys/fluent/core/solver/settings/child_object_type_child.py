#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class child_object_type_child(Group):
    """'child_object_type' of child_object_type."""

    fluent_name = "child-object-type"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of child_object_type_child
    """
    constant: constant = constant
    """
    constant child of child_object_type_child
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of child_object_type_child
    """
    field_name: field_name = field_name
    """
    field_name child of child_object_type_child
    """
    udf: udf = udf
    """
    udf child of child_object_type_child
    """
