#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class fvar2(Group):
    """
    'fvar2' child.
    """

    fluent_name = "fvar2"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of fvar2
    """
    constant: constant = constant
    """
    constant child of fvar2
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of fvar2
    """
    field_name: field_name = field_name
    """
    field_name child of fvar2
    """
    udf: udf = udf
    """
    udf child of fvar2
    """
