#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .expert import expert
from .relative_convergence_criterion import relative_convergence_criterion
from .max_iterations_per_timestep import max_iterations_per_timestep
class acoustics_wave_equation_controls(Group):
    """
    'acoustics_wave_equation_controls' child.
    """

    fluent_name = "acoustics-wave-equation-controls"

    child_names = \
        ['expert', 'relative_convergence_criterion',
         'max_iterations_per_timestep']

    expert: expert = expert
    """
    expert child of acoustics_wave_equation_controls
    """
    relative_convergence_criterion: relative_convergence_criterion = relative_convergence_criterion
    """
    relative_convergence_criterion child of acoustics_wave_equation_controls
    """
    max_iterations_per_timestep: max_iterations_per_timestep = max_iterations_per_timestep
    """
    max_iterations_per_timestep child of acoustics_wave_equation_controls
    """
