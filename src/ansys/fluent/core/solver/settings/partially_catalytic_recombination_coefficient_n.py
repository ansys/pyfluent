#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class partially_catalytic_recombination_coefficient_n(Group):
    """
    'partially_catalytic_recombination_coefficient_n' child.
    """

    fluent_name = "partially-catalytic-recombination-coefficient-n"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of partially_catalytic_recombination_coefficient_n
    """
    constant: constant = constant
    """
    constant child of partially_catalytic_recombination_coefficient_n
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of partially_catalytic_recombination_coefficient_n
    """
    field_name: field_name = field_name
    """
    field_name child of partially_catalytic_recombination_coefficient_n
    """
    udf: udf = udf
    """
    udf child of partially_catalytic_recombination_coefficient_n
    """
