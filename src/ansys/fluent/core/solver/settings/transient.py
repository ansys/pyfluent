#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .transient_parameters_specify import transient_parameters_specify
from .transient_scheme import transient_scheme
from .time_scale_modification_method import time_scale_modification_method
from .time_scale_modification_factor import time_scale_modification_factor
class transient(Group):
    """
    'transient' child.
    """

    fluent_name = "transient"

    child_names = \
        ['transient_parameters_specify', 'transient_scheme',
         'time_scale_modification_method', 'time_scale_modification_factor']

    transient_parameters_specify: transient_parameters_specify = transient_parameters_specify
    """
    transient_parameters_specify child of transient
    """
    transient_scheme: transient_scheme = transient_scheme
    """
    transient_scheme child of transient
    """
    time_scale_modification_method: time_scale_modification_method = time_scale_modification_method
    """
    time_scale_modification_method child of transient
    """
    time_scale_modification_factor: time_scale_modification_factor = time_scale_modification_factor
    """
    time_scale_modification_factor child of transient
    """
