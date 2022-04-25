#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .constant import constant
from .field_name import field_name
from .option import option
from .profile_name import profile_name
from .udf import udf


class wave_spect_mean_angle(Group):
    """'wave_spect_mean_angle' child."""

    fluent_name = "wave-spect-mean-angle"

    child_names = ["option", "constant", "profile_name", "field_name", "udf"]

    option: option = option
    """
    option child of wave_spect_mean_angle
    """
    constant: constant = constant
    """
    constant child of wave_spect_mean_angle
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of wave_spect_mean_angle
    """
    field_name: field_name = field_name
    """
    field_name child of wave_spect_mean_angle
    """
    udf: udf = udf
    """
    udf child of wave_spect_mean_angle
    """
