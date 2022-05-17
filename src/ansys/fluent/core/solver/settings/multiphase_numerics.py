#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .porous_media import porous_media
from .compressible_flow import compressible_flow
from .boiling_parameters import boiling_parameters
from .viscous_flow import viscous_flow
from .heat_mass_transfer import heat_mass_transfer
from .advanced_stability_controls import advanced_stability_controls
from .default_controls import default_controls
from .face_pressure_controls import face_pressure_controls
from .solution_stabilization_1 import solution_stabilization
class multiphase_numerics(Group):
    """
    Enter the multiphase numerics options menu.
    """

    fluent_name = "multiphase-numerics"

    child_names = \
        ['porous_media', 'compressible_flow', 'boiling_parameters',
         'viscous_flow', 'heat_mass_transfer', 'advanced_stability_controls',
         'default_controls', 'face_pressure_controls',
         'solution_stabilization']

    porous_media: porous_media = porous_media
    """
    porous_media child of multiphase_numerics
    """
    compressible_flow: compressible_flow = compressible_flow
    """
    compressible_flow child of multiphase_numerics
    """
    boiling_parameters: boiling_parameters = boiling_parameters
    """
    boiling_parameters child of multiphase_numerics
    """
    viscous_flow: viscous_flow = viscous_flow
    """
    viscous_flow child of multiphase_numerics
    """
    heat_mass_transfer: heat_mass_transfer = heat_mass_transfer
    """
    heat_mass_transfer child of multiphase_numerics
    """
    advanced_stability_controls: advanced_stability_controls = advanced_stability_controls
    """
    advanced_stability_controls child of multiphase_numerics
    """
    default_controls: default_controls = default_controls
    """
    default_controls child of multiphase_numerics
    """
    face_pressure_controls: face_pressure_controls = face_pressure_controls
    """
    face_pressure_controls child of multiphase_numerics
    """
    solution_stabilization: solution_stabilization = solution_stabilization
    """
    solution_stabilization child of multiphase_numerics
    """
