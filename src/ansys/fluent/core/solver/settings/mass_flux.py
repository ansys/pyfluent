#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class mass_flux(Group):
    """
    'mass_flux' child.
    """

    fluent_name = "mass-flux"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of mass_flux
    """
    constant: constant = constant
    """
    constant child of mass_flux
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of mass_flux
    """
    field_name: field_name = field_name
    """
    field_name child of mass_flux
    """
    udf: udf = udf
    """
    udf child of mass_flux
    """
