#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class heading_angle(Group):
    """
    'heading_angle' child.
    """

    fluent_name = "heading-angle"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of heading_angle
    """
    constant: constant = constant
    """
    constant child of heading_angle
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of heading_angle
    """
    field_name: field_name = field_name
    """
    field_name child of heading_angle
    """
    udf: udf = udf
    """
    udf child of heading_angle
    """
