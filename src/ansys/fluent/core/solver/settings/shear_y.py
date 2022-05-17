#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class shear_y(Group):
    """
    'shear_y' child.
    """

    fluent_name = "shear-y"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of shear_y
    """
    constant: constant = constant
    """
    constant child of shear_y
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of shear_y
    """
    field_name: field_name = field_name
    """
    field_name child of shear_y
    """
    udf: udf = udf
    """
    udf child of shear_y
    """
