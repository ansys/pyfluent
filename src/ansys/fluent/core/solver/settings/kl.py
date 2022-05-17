#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class kl(Group):
    """
    'kl' child.
    """

    fluent_name = "kl"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of kl
    """
    constant: constant = constant
    """
    constant child of kl
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of kl
    """
    field_name: field_name = field_name
    """
    field_name child of kl
    """
    udf: udf = udf
    """
    udf child of kl
    """
