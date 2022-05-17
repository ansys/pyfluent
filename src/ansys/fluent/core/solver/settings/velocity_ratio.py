#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class velocity_ratio(Group):
    """
    'velocity_ratio' child.
    """

    fluent_name = "velocity-ratio"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of velocity_ratio
    """
    constant: constant = constant
    """
    constant child of velocity_ratio
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of velocity_ratio
    """
    field_name: field_name = field_name
    """
    field_name child of velocity_ratio
    """
    udf: udf = udf
    """
    udf child of velocity_ratio
    """
