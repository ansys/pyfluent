#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .type import type
from .two_dim_space import two_dim_space
from .velocity_formulation import velocity_formulation
from .time import time
class solver(Group):
    """
    'solver' child.
    """

    fluent_name = "solver"

    child_names = \
        ['type', 'two_dim_space', 'velocity_formulation', 'time']

    type: type = type
    """
    type child of solver
    """
    two_dim_space: two_dim_space = two_dim_space
    """
    two_dim_space child of solver
    """
    velocity_formulation: velocity_formulation = velocity_formulation
    """
    velocity_formulation child of solver
    """
    time: time = time
    """
    time child of solver
    """
