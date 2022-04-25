#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class droplet_diameter(Group):
    """'droplet_diameter' child."""

    fluent_name = "droplet-diameter"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of droplet_diameter
    """
    constant: constant = constant
    """
    constant child of droplet_diameter
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of droplet_diameter
    """
    field_name: field_name = field_name
    """
    field_name child of droplet_diameter
    """
    udf: udf = udf
    """
    udf child of droplet_diameter
    """
