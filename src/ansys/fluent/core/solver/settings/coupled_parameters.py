#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .fixed_cycle_parameters_1 import fixed_cycle_parameters
from .coarsening_parameters_1 import coarsening_parameters
from .smoother_type_1 import smoother_type
class coupled_parameters(Group):
    """
    'coupled_parameters' child.
    """

    fluent_name = "coupled-parameters"

    child_names = \
        ['fixed_cycle_parameters', 'coarsening_parameters', 'smoother_type']

    fixed_cycle_parameters: fixed_cycle_parameters = fixed_cycle_parameters
    """
    fixed_cycle_parameters child of coupled_parameters
    """
    coarsening_parameters: coarsening_parameters = coarsening_parameters
    """
    coarsening_parameters child of coupled_parameters
    """
    smoother_type: smoother_type = smoother_type
    """
    smoother_type child of coupled_parameters
    """
