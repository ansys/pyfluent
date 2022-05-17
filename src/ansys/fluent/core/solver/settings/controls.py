#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .acoustics_wave_equation_controls import acoustics_wave_equation_controls
from .advanced import advanced
from .contact_solution_controls import contact_solution_controls
from .courant_number import courant_number
from .equations import equations
from .limits import limits
from .p_v_controls import p_v_controls
from .relaxation_factor_1 import relaxation_factor
from .set_controls_to_default import set_controls_to_default
from .under_relaxation import under_relaxation
class controls(Group):
    """
    'controls' child.
    """

    fluent_name = "controls"

    child_names = \
        ['acoustics_wave_equation_controls', 'advanced',
         'contact_solution_controls', 'courant_number', 'equations', 'limits',
         'p_v_controls', 'relaxation_factor', 'set_controls_to_default',
         'under_relaxation']

    acoustics_wave_equation_controls: acoustics_wave_equation_controls = acoustics_wave_equation_controls
    """
    acoustics_wave_equation_controls child of controls
    """
    advanced: advanced = advanced
    """
    advanced child of controls
    """
    contact_solution_controls: contact_solution_controls = contact_solution_controls
    """
    contact_solution_controls child of controls
    """
    courant_number: courant_number = courant_number
    """
    courant_number child of controls
    """
    equations: equations = equations
    """
    equations child of controls
    """
    limits: limits = limits
    """
    limits child of controls
    """
    p_v_controls: p_v_controls = p_v_controls
    """
    p_v_controls child of controls
    """
    relaxation_factor: relaxation_factor = relaxation_factor
    """
    relaxation_factor child of controls
    """
    set_controls_to_default: set_controls_to_default = set_controls_to_default
    """
    set_controls_to_default child of controls
    """
    under_relaxation: under_relaxation = under_relaxation
    """
    under_relaxation child of controls
    """
