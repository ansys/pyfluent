#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class trad(Group):
    """
    'trad' child.
    """

    fluent_name = "trad"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of trad
    """
    constant: constant = constant
    """
    constant child of trad
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of trad
    """
    field_name: field_name = field_name
    """
    field_name child of trad
    """
    udf: udf = udf
    """
    udf child of trad
    """
