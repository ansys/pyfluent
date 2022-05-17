#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class per_dispx(Group):
    """
    'per_dispx' child.
    """

    fluent_name = "per-dispx"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of per_dispx
    """
    constant: constant = constant
    """
    constant child of per_dispx
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of per_dispx
    """
    field_name: field_name = field_name
    """
    field_name child of per_dispx
    """
    udf: udf = udf
    """
    udf child of per_dispx
    """
