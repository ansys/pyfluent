#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class elec_potential_jump(Group):
    """'elec_potential_jump' child."""

    fluent_name = "elec-potential-jump"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of elec_potential_jump
    """
    constant: constant = constant
    """
    constant child of elec_potential_jump
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of elec_potential_jump
    """
    field_name: field_name = field_name
    """
    field_name child of elec_potential_jump
    """
    udf: udf = udf
    """
    udf child of elec_potential_jump
    """
