#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class ec_mass_flow(Group):
    """'ec_mass_flow' child."""

    fluent_name = "ec-mass-flow"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of ec_mass_flow
    """
    constant: constant = constant
    """
    constant child of ec_mass_flow
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ec_mass_flow
    """
    field_name: field_name = field_name
    """
    field_name child of ec_mass_flow
    """
    udf: udf = udf
    """
    udf child of ec_mass_flow
    """
