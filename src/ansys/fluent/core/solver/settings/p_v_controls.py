#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .skewness_correction_itr import skewness_correction_itr
from .neighbor_correction_itr import neighbor_correction_itr
from .skewness_neighbor_coupling import skewness_neighbor_coupling
from .vof_correction_itr import vof_correction_itr
from .explicit_momentum_under_relaxation import explicit_momentum_under_relaxation
from .explicit_pressure_under_relaxation import explicit_pressure_under_relaxation
from .flow_courant_number import flow_courant_number
from .volume_fraction_courant_number import volume_fraction_courant_number
from .explicit_volume_fraction_under_relaxation import explicit_volume_fraction_under_relaxation
class p_v_controls(Group):
    """
    'p_v_controls' child.
    """

    fluent_name = "p-v-controls"

    child_names = \
        ['skewness_correction_itr', 'neighbor_correction_itr',
         'skewness_neighbor_coupling', 'vof_correction_itr',
         'explicit_momentum_under_relaxation',
         'explicit_pressure_under_relaxation', 'flow_courant_number',
         'volume_fraction_courant_number',
         'explicit_volume_fraction_under_relaxation']

    skewness_correction_itr: skewness_correction_itr = skewness_correction_itr
    """
    skewness_correction_itr child of p_v_controls
    """
    neighbor_correction_itr: neighbor_correction_itr = neighbor_correction_itr
    """
    neighbor_correction_itr child of p_v_controls
    """
    skewness_neighbor_coupling: skewness_neighbor_coupling = skewness_neighbor_coupling
    """
    skewness_neighbor_coupling child of p_v_controls
    """
    vof_correction_itr: vof_correction_itr = vof_correction_itr
    """
    vof_correction_itr child of p_v_controls
    """
    explicit_momentum_under_relaxation: explicit_momentum_under_relaxation = explicit_momentum_under_relaxation
    """
    explicit_momentum_under_relaxation child of p_v_controls
    """
    explicit_pressure_under_relaxation: explicit_pressure_under_relaxation = explicit_pressure_under_relaxation
    """
    explicit_pressure_under_relaxation child of p_v_controls
    """
    flow_courant_number: flow_courant_number = flow_courant_number
    """
    flow_courant_number child of p_v_controls
    """
    volume_fraction_courant_number: volume_fraction_courant_number = volume_fraction_courant_number
    """
    volume_fraction_courant_number child of p_v_controls
    """
    explicit_volume_fraction_under_relaxation: explicit_volume_fraction_under_relaxation = explicit_volume_fraction_under_relaxation
    """
    explicit_volume_fraction_under_relaxation child of p_v_controls
    """
