#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .coupled_solver import coupled_solver
from .segregated_solver import segregated_solver
from .density_based_solver import density_based_solver
class formulation(Group):
    """
    'formulation' child.
    """

    fluent_name = "formulation"

    child_names = \
        ['coupled_solver', 'segregated_solver', 'density_based_solver']

    coupled_solver: coupled_solver = coupled_solver
    """
    coupled_solver child of formulation
    """
    segregated_solver: segregated_solver = segregated_solver
    """
    segregated_solver child of formulation
    """
    density_based_solver: density_based_solver = density_based_solver
    """
    density_based_solver child of formulation
    """
