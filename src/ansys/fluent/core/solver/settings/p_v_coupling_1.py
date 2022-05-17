#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .flow_scheme import flow_scheme
from .coupled_form import coupled_form
from .solve_n_phase import solve_n_phase
class p_v_coupling(Group):
    """
    'p_v_coupling' child.
    """

    fluent_name = "p-v-coupling"

    child_names = \
        ['flow_scheme', 'coupled_form', 'solve_n_phase']

    flow_scheme: flow_scheme = flow_scheme
    """
    flow_scheme child of p_v_coupling
    """
    coupled_form: coupled_form = coupled_form
    """
    coupled_form child of p_v_coupling
    """
    solve_n_phase: solve_n_phase = solve_n_phase
    """
    solve_n_phase child of p_v_coupling
    """
