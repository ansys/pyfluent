#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .max_coarse_levels_1 import max_coarse_levels
from .coarsen_by_interval_1 import coarsen_by_interval
from .conservative_coarsening import conservative_coarsening
from .aggressive_coarsening_1 import aggressive_coarsening
from .laplace_coarsening import laplace_coarsening
class coarsening_parameters(Group):
    """
    'coarsening_parameters' child.
    """

    fluent_name = "coarsening-parameters"

    child_names = \
        ['max_coarse_levels', 'coarsen_by_interval',
         'conservative_coarsening', 'aggressive_coarsening',
         'laplace_coarsening']

    max_coarse_levels: max_coarse_levels = max_coarse_levels
    """
    max_coarse_levels child of coarsening_parameters
    """
    coarsen_by_interval: coarsen_by_interval = coarsen_by_interval
    """
    coarsen_by_interval child of coarsening_parameters
    """
    conservative_coarsening: conservative_coarsening = conservative_coarsening
    """
    conservative_coarsening child of coarsening_parameters
    """
    aggressive_coarsening: aggressive_coarsening = aggressive_coarsening
    """
    aggressive_coarsening child of coarsening_parameters
    """
    laplace_coarsening: laplace_coarsening = laplace_coarsening
    """
    laplace_coarsening child of coarsening_parameters
    """
