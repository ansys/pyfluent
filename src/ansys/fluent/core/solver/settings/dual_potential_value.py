#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class dual_potential_value(Group):
    """
    'dual_potential_value' child.
    """

    fluent_name = "dual-potential-value"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of dual_potential_value
    """
    constant: constant = constant
    """
    constant child of dual_potential_value
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of dual_potential_value
    """
    field_name: field_name = field_name
    """
    field_name child of dual_potential_value
    """
    udf: udf = udf
    """
    udf child of dual_potential_value
    """
