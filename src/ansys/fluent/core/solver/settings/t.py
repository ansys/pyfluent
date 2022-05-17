#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class t(Group):
    """
    't' child.
    """

    fluent_name = "t"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of t
    """
    constant: constant = constant
    """
    constant child of t
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of t
    """
    field_name: field_name = field_name
    """
    field_name child of t
    """
    udf: udf = udf
    """
    udf child of t
    """
