#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class phase_diff(Group):
    """
    'phase_diff' child.
    """

    fluent_name = "phase-diff"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of phase_diff
    """
    constant: constant = constant
    """
    constant child of phase_diff
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of phase_diff
    """
    field_name: field_name = field_name
    """
    field_name child of phase_diff
    """
    udf: udf = udf
    """
    udf child of phase_diff
    """
