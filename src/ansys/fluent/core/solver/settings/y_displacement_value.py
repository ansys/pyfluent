#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class y_displacement_value(Group):
    """
    'y_displacement_value' child.
    """

    fluent_name = "y-displacement-value"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of y_displacement_value
    """
    constant: constant = constant
    """
    constant child of y_displacement_value
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of y_displacement_value
    """
    field_name: field_name = field_name
    """
    field_name child of y_displacement_value
    """
    udf: udf = udf
    """
    udf child of y_displacement_value
    """
