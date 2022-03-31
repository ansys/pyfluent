#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class film_temperature(Group):
    """'film_temperature' child."""

    fluent_name = "film-temperature"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of film_temperature
    """
    constant: constant = constant
    """
    constant child of film_temperature
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of film_temperature
    """
    field_name: field_name = field_name
    """
    field_name child of film_temperature
    """
    udf: udf = udf
    """
    udf child of film_temperature
    """
