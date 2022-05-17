#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .convergence_acc_std_meshes import convergence_acc_std_meshes
from .enhanced_casm_formulation import enhanced_casm_formulation
from .casm_cutoff_multiplier import casm_cutoff_multiplier
from .disable_casm import disable_casm
class convergence_acceleration_for_stretched_meshes(Group):
    """
    'convergence_acceleration_for_stretched_meshes' child.
    """

    fluent_name = "convergence-acceleration-for-stretched-meshes"

    child_names = \
        ['convergence_acc_std_meshes', 'enhanced_casm_formulation',
         'casm_cutoff_multiplier']

    convergence_acc_std_meshes: convergence_acc_std_meshes = convergence_acc_std_meshes
    """
    convergence_acc_std_meshes child of convergence_acceleration_for_stretched_meshes
    """
    enhanced_casm_formulation: enhanced_casm_formulation = enhanced_casm_formulation
    """
    enhanced_casm_formulation child of convergence_acceleration_for_stretched_meshes
    """
    casm_cutoff_multiplier: casm_cutoff_multiplier = casm_cutoff_multiplier
    """
    casm_cutoff_multiplier child of convergence_acceleration_for_stretched_meshes
    """
    command_names = \
        ['disable_casm']

    disable_casm: disable_casm = disable_casm
    """
    disable_casm command of convergence_acceleration_for_stretched_meshes
    """
