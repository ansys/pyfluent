#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .enable_dynamic_strength import enable_dynamic_strength
from .set_dynamic_strength_exponent import set_dynamic_strength_exponent
from .set_maximum_dynamic_strength import set_maximum_dynamic_strength


class anti_diffusion(Group):
    """'anti_diffusion' child."""

    fluent_name = "anti-diffusion"

    child_names = [
        "enable_dynamic_strength",
        "set_dynamic_strength_exponent",
        "set_maximum_dynamic_strength",
    ]

    enable_dynamic_strength: enable_dynamic_strength = enable_dynamic_strength
    """
    enable_dynamic_strength child of anti_diffusion
    """
    set_dynamic_strength_exponent: set_dynamic_strength_exponent = (
        set_dynamic_strength_exponent
    )
    """
    set_dynamic_strength_exponent child of anti_diffusion
    """
    set_maximum_dynamic_strength: set_maximum_dynamic_strength = (
        set_maximum_dynamic_strength
    )
    """
    set_maximum_dynamic_strength child of anti_diffusion
    """
