#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class x_velocity(Group):
    """
    'x_velocity' child.
    """

    fluent_name = "x-velocity"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of x_velocity
    """
    constant: constant = constant
    """
    constant child of x_velocity
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of x_velocity
    """
    field_name: field_name = field_name
    """
    field_name child of x_velocity
    """
    udf: udf = udf
    """
    udf child of x_velocity
    """
