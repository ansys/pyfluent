#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enable_3 import enable
from .turbulence_options import turbulence_options


class warped_face_gradient_correction(Group):
    """'warped_face_gradient_correction' child."""

    fluent_name = "warped-face-gradient-correction"

    child_names = ["enable", "turbulence_options"]

    enable: enable = enable
    """
    enable child of warped_face_gradient_correction
    """
    turbulence_options: turbulence_options = turbulence_options
    """
    turbulence_options child of warped_face_gradient_correction
    """
