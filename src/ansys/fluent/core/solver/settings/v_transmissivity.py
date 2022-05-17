#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class v_transmissivity(Group):
    """
    'v_transmissivity' child.
    """

    fluent_name = "v-transmissivity"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of v_transmissivity
    """
    constant: constant = constant
    """
    constant child of v_transmissivity
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of v_transmissivity
    """
    field_name: field_name = field_name
    """
    field_name child of v_transmissivity
    """
    udf: udf = udf
    """
    udf child of v_transmissivity
    """
