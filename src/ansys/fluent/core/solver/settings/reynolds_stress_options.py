#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .solve_tke import solve_tke
from .wall_echo import wall_echo
class reynolds_stress_options(Group):
    """
    'reynolds_stress_options' child.
    """

    fluent_name = "reynolds-stress-options"

    child_names = \
        ['solve_tke', 'wall_echo']

    solve_tke: solve_tke = solve_tke
    """
    solve_tke child of reynolds_stress_options
    """
    wall_echo: wall_echo = wall_echo
    """
    wall_echo child of reynolds_stress_options
    """
