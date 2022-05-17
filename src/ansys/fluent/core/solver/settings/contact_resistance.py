#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class contact_resistance(Group):
    """
    'contact_resistance' child.
    """

    fluent_name = "contact-resistance"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of contact_resistance
    """
    constant: constant = constant
    """
    constant child of contact_resistance
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of contact_resistance
    """
    field_name: field_name = field_name
    """
    field_name child of contact_resistance
    """
    udf: udf = udf
    """
    udf child of contact_resistance
    """
