#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class li_ion_value(Group):
    """'li_ion_value' child."""

    fluent_name = "li-ion-value"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of li_ion_value
    """
    constant: constant = constant
    """
    constant child of li_ion_value
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of li_ion_value
    """
    field_name: field_name = field_name
    """
    field_name child of li_ion_value
    """
    udf: udf = udf
    """
    udf child of li_ion_value
    """
