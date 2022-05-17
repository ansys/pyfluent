#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class wave_ht(Group):
    """
    'wave_ht' child.
    """

    fluent_name = "wave-ht"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of wave_ht
    """
    constant: constant = constant
    """
    constant child of wave_ht
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of wave_ht
    """
    field_name: field_name = field_name
    """
    field_name child of wave_ht
    """
    udf: udf = udf
    """
    udf child of wave_ht
    """
