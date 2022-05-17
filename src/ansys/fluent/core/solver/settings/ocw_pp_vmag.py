#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class ocw_pp_vmag(Group):
    """
    'ocw_pp_vmag' child.
    """

    fluent_name = "ocw-pp-vmag"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of ocw_pp_vmag
    """
    constant: constant = constant
    """
    constant child of ocw_pp_vmag
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ocw_pp_vmag
    """
    field_name: field_name = field_name
    """
    field_name child of ocw_pp_vmag
    """
    udf: udf = udf
    """
    udf child of ocw_pp_vmag
    """
