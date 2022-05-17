#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class porous_c_3(Group):
    """
    'porous_c_3' child.
    """

    fluent_name = "porous-c-3"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of porous_c_3
    """
    constant: constant = constant
    """
    constant child of porous_c_3
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of porous_c_3
    """
    field_name: field_name = field_name
    """
    field_name child of porous_c_3
    """
    udf: udf = udf
    """
    udf child of porous_c_3
    """
