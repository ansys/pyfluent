#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class pollut_hg(Group):
    """
    'pollut_hg' child.
    """

    fluent_name = "pollut-hg"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of pollut_hg
    """
    constant: constant = constant
    """
    constant child of pollut_hg
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of pollut_hg
    """
    field_name: field_name = field_name
    """
    field_name child of pollut_hg
    """
    udf: udf = udf
    """
    udf child of pollut_hg
    """
