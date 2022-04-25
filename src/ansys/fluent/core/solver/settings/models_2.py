#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .model_ramping import model_ramping
from .ramp_flow import ramp_flow
from .ramp_scalars import ramp_scalars
from .ramp_turbulence import ramp_turbulence


class models(Group):
    """'models' child."""

    fluent_name = "models"

    child_names = [
        "model_ramping",
        "ramp_flow",
        "ramp_turbulence",
        "ramp_scalars",
    ]

    model_ramping: model_ramping = model_ramping
    """
    model_ramping child of models
    """
    ramp_flow: ramp_flow = ramp_flow
    """
    ramp_flow child of models
    """
    ramp_turbulence: ramp_turbulence = ramp_turbulence
    """
    ramp_turbulence child of models
    """
    ramp_scalars: ramp_scalars = ramp_scalars
    """
    ramp_scalars child of models
    """
