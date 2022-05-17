#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class shear_z(Group):
    """
    'shear_z' child.
    """

    fluent_name = "shear-z"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of shear_z
    """
    constant: constant = constant
    """
    constant child of shear_z
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of shear_z
    """
    field_name: field_name = field_name
    """
    field_name child of shear_z
    """
    udf: udf = udf
    """
    udf child of shear_z
    """
