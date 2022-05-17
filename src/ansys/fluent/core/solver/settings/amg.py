#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enforce_laplace_coarsening import enforce_laplace_coarsening
from .increase_pre_sweeps import increase_pre_sweeps
from .pre_sweeps_3 import pre_sweeps
from .specify_coarsening_rate import specify_coarsening_rate
from .coarsen_rate import coarsen_rate
class amg(Group):
    """
    'amg' child.
    """

    fluent_name = "amg"

    child_names = \
        ['enforce_laplace_coarsening', 'increase_pre_sweeps', 'pre_sweeps',
         'specify_coarsening_rate', 'coarsen_rate']

    enforce_laplace_coarsening: enforce_laplace_coarsening = enforce_laplace_coarsening
    """
    enforce_laplace_coarsening child of amg
    """
    increase_pre_sweeps: increase_pre_sweeps = increase_pre_sweeps
    """
    increase_pre_sweeps child of amg
    """
    pre_sweeps: pre_sweeps = pre_sweeps
    """
    pre_sweeps child of amg
    """
    specify_coarsening_rate: specify_coarsening_rate = specify_coarsening_rate
    """
    specify_coarsening_rate child of amg
    """
    coarsen_rate: coarsen_rate = coarsen_rate
    """
    coarsen_rate child of amg
    """
