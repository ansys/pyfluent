#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class variable_roughness(Group):
    """
    'variable_roughness' child.
    """

    fluent_name = "variable-roughness"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of variable_roughness
    """
    constant: constant = constant
    """
    constant child of variable_roughness
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of variable_roughness
    """
    field_name: field_name = field_name
    """
    field_name child of variable_roughness
    """
    udf: udf = udf
    """
    udf child of variable_roughness
    """
