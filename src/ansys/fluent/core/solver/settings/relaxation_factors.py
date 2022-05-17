#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .local_dt_dualts_relax import local_dt_dualts_relax
from .global_dt_pseudo_relax import global_dt_pseudo_relax
class relaxation_factors(Group):
    """
    'relaxation_factors' child.
    """

    fluent_name = "relaxation-factors"

    child_names = \
        ['local_dt_dualts_relax', 'global_dt_pseudo_relax']

    local_dt_dualts_relax: local_dt_dualts_relax = local_dt_dualts_relax
    """
    local_dt_dualts_relax child of relaxation_factors
    """
    global_dt_pseudo_relax: global_dt_pseudo_relax = global_dt_pseudo_relax
    """
    global_dt_pseudo_relax child of relaxation_factors
    """
