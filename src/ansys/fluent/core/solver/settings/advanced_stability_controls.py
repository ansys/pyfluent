#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .pseudo_transient import pseudo_transient
from .p_v_coupling import p_v_coupling
from .hybrid_nita import hybrid_nita
from .equation_order import equation_order
from .anti_diffusion import anti_diffusion
class advanced_stability_controls(Group):
    """
    'advanced_stability_controls' child.
    """

    fluent_name = "advanced-stability-controls"

    child_names = \
        ['pseudo_transient', 'p_v_coupling', 'hybrid_nita', 'equation_order',
         'anti_diffusion']

    pseudo_transient: pseudo_transient = pseudo_transient
    """
    pseudo_transient child of advanced_stability_controls
    """
    p_v_coupling: p_v_coupling = p_v_coupling
    """
    p_v_coupling child of advanced_stability_controls
    """
    hybrid_nita: hybrid_nita = hybrid_nita
    """
    hybrid_nita child of advanced_stability_controls
    """
    equation_order: equation_order = equation_order
    """
    equation_order child of advanced_stability_controls
    """
    anti_diffusion: anti_diffusion = anti_diffusion
    """
    anti_diffusion child of advanced_stability_controls
    """
