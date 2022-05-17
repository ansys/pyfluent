#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class avg_flow_velocity(Group):
    """
    'avg_flow_velocity' child.
    """

    fluent_name = "avg-flow-velocity"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of avg_flow_velocity
    """
    constant: constant = constant
    """
    constant child of avg_flow_velocity
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of avg_flow_velocity
    """
    field_name: field_name = field_name
    """
    field_name child of avg_flow_velocity
    """
    udf: udf = udf
    """
    udf child of avg_flow_velocity
    """
