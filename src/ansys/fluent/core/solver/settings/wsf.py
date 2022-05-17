#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class wsf(Group):
    """
    'wsf' child.
    """

    fluent_name = "wsf"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of wsf
    """
    constant: constant = constant
    """
    constant child of wsf
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of wsf
    """
    field_name: field_name = field_name
    """
    field_name child of wsf
    """
    udf: udf = udf
    """
    udf child of wsf
    """
