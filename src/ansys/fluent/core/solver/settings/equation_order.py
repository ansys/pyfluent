#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .solve_flow_last import solve_flow_last
from .solve_exp_vof_at_end import solve_exp_vof_at_end
class equation_order(Group):
    """
    'equation_order' child.
    """

    fluent_name = "equation-order"

    child_names = \
        ['solve_flow_last', 'solve_exp_vof_at_end']

    solve_flow_last: solve_flow_last = solve_flow_last
    """
    solve_flow_last child of equation_order
    """
    solve_exp_vof_at_end: solve_exp_vof_at_end = solve_exp_vof_at_end
    """
    solve_exp_vof_at_end child of equation_order
    """
