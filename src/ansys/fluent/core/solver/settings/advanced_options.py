#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .local_dt import local_dt
from .global_dt import global_dt
class advanced_options(Group):
    """
    'advanced_options' child.
    """

    fluent_name = "advanced-options"

    child_names = \
        ['local_dt', 'global_dt']

    local_dt: local_dt = local_dt
    """
    local_dt child of advanced_options
    """
    global_dt: global_dt = global_dt
    """
    global_dt child of advanced_options
    """
