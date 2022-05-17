#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class supersonic_or_initial_gauge_pressure(Group):
    """
    'supersonic_or_initial_gauge_pressure' child.
    """

    fluent_name = "supersonic-or-initial-gauge-pressure"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of supersonic_or_initial_gauge_pressure
    """
    constant: constant = constant
    """
    constant child of supersonic_or_initial_gauge_pressure
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of supersonic_or_initial_gauge_pressure
    """
    field_name: field_name = field_name
    """
    field_name child of supersonic_or_initial_gauge_pressure
    """
    udf: udf = udf
    """
    udf child of supersonic_or_initial_gauge_pressure
    """
