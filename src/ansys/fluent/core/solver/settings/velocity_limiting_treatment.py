#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enable_velocity_limiting import enable_velocity_limiting
from .set_velocity_and_vof_cutoffs import set_velocity_and_vof_cutoffs
from .set_damping_strengths import set_damping_strengths
from .set_velocity_cutoff import set_velocity_cutoff
from .set_damping_strength import set_damping_strength
from .verbosity_2 import verbosity
class velocity_limiting_treatment(Group):
    """
    'velocity_limiting_treatment' child.
    """

    fluent_name = "velocity-limiting-treatment"

    child_names = \
        ['enable_velocity_limiting', 'set_velocity_and_vof_cutoffs',
         'set_damping_strengths', 'set_velocity_cutoff',
         'set_damping_strength', 'verbosity']

    enable_velocity_limiting: enable_velocity_limiting = enable_velocity_limiting
    """
    enable_velocity_limiting child of velocity_limiting_treatment
    """
    set_velocity_and_vof_cutoffs: set_velocity_and_vof_cutoffs = set_velocity_and_vof_cutoffs
    """
    set_velocity_and_vof_cutoffs child of velocity_limiting_treatment
    """
    set_damping_strengths: set_damping_strengths = set_damping_strengths
    """
    set_damping_strengths child of velocity_limiting_treatment
    """
    set_velocity_cutoff: set_velocity_cutoff = set_velocity_cutoff
    """
    set_velocity_cutoff child of velocity_limiting_treatment
    """
    set_damping_strength: set_damping_strength = set_damping_strength
    """
    set_damping_strength child of velocity_limiting_treatment
    """
    verbosity: verbosity = verbosity
    """
    verbosity child of velocity_limiting_treatment
    """
