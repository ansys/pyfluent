#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class liquid_content_cp(Group):
    """
    'liquid_content_cp' child.
    """

    fluent_name = "liquid-content-cp"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of liquid_content_cp
    """
    constant: constant = constant
    """
    constant child of liquid_content_cp
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of liquid_content_cp
    """
    field_name: field_name = field_name
    """
    field_name child of liquid_content_cp
    """
    udf: udf = udf
    """
    udf child of liquid_content_cp
    """
