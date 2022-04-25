#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class film_cond_rate(Group):
    """'film_cond_rate' child."""

    fluent_name = "film-cond-rate"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of film_cond_rate
    """
    constant: constant = constant
    """
    constant child of film_cond_rate
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of film_cond_rate
    """
    field_name: field_name = field_name
    """
    field_name child of film_cond_rate
    """
    udf: udf = udf
    """
    udf child of film_cond_rate
    """
