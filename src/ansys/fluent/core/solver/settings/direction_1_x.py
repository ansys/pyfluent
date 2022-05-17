#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class direction_1_x(Group):
    """
    'direction_1_x' child.
    """

    fluent_name = "direction-1-x"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of direction_1_x
    """
    constant: constant = constant
    """
    constant child of direction_1_x
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of direction_1_x
    """
    field_name: field_name = field_name
    """
    field_name child of direction_1_x
    """
    udf: udf = udf
    """
    udf child of direction_1_x
    """
