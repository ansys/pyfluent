#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .solver import solver
from .adjust_solver_defaults_based_on_setup import adjust_solver_defaults_based_on_setup
from .gravity_1 import gravity
class general(Group):
    """
    'general' child.
    """

    fluent_name = "general"

    child_names = \
        ['solver', 'adjust_solver_defaults_based_on_setup', 'gravity']

    solver: solver = solver
    """
    solver child of general
    """
    adjust_solver_defaults_based_on_setup: adjust_solver_defaults_based_on_setup = adjust_solver_defaults_based_on_setup
    """
    adjust_solver_defaults_based_on_setup child of general
    """
    gravity: gravity = gravity
    """
    gravity child of general
    """
