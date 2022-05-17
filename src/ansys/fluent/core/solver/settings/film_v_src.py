#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class film_v_src(Group):
    """
    'film_v_src' child.
    """

    fluent_name = "film-v-src"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of film_v_src
    """
    constant: constant = constant
    """
    constant child of film_v_src
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of film_v_src
    """
    field_name: field_name = field_name
    """
    field_name child of film_v_src
    """
    udf: udf = udf
    """
    udf child of film_v_src
    """
