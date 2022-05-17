#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class vr_profile(Group):
    """
    'vr_profile' child.
    """

    fluent_name = "vr-profile"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of vr_profile
    """
    constant: constant = constant
    """
    constant child of vr_profile
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of vr_profile
    """
    field_name: field_name = field_name
    """
    field_name child of vr_profile
    """
    udf: udf = udf
    """
    udf child of vr_profile
    """
