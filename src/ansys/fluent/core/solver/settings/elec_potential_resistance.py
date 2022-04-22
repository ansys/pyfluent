#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class elec_potential_resistance(Group):
    """'elec_potential_resistance' child."""

    fluent_name = "elec-potential-resistance"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of elec_potential_resistance
    """
    constant: constant = constant
    """
    constant child of elec_potential_resistance
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of elec_potential_resistance
    """
    field_name: field_name = field_name
    """
    field_name child of elec_potential_resistance
    """
    udf: udf = udf
    """
    udf child of elec_potential_resistance
    """
