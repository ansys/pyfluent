#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .area import area
from .compute_1 import compute
from .density_1 import density
from .depth import depth
from .enthalpy import enthalpy
from .length_val import length_val
from .list_val import list_val
from .pressure import pressure
from .temperature_1 import temperature
from .velocity import velocity
from .viscosity_1 import viscosity
from .yplus import yplus


class reference_values(Group):
    """'reference_values' child."""

    fluent_name = "reference-values"

    child_names = [
        "area",
        "compute",
        "depth",
        "density",
        "enthalpy",
        "length_val",
        "pressure",
        "temperature",
        "yplus",
        "velocity",
        "viscosity",
        "list_val",
    ]

    area: area = area
    """
    area child of reference_values
    """
    compute: compute = compute
    """
    compute child of reference_values
    """
    depth: depth = depth
    """
    depth child of reference_values
    """
    density: density = density
    """
    density child of reference_values
    """
    enthalpy: enthalpy = enthalpy
    """
    enthalpy child of reference_values
    """
    length_val: length_val = length_val
    """
    length_val child of reference_values
    """
    pressure: pressure = pressure
    """
    pressure child of reference_values
    """
    temperature: temperature = temperature
    """
    temperature child of reference_values
    """
    yplus: yplus = yplus
    """
    yplus child of reference_values
    """
    velocity: velocity = velocity
    """
    velocity child of reference_values
    """
    viscosity: viscosity = viscosity
    """
    viscosity child of reference_values
    """
    list_val: list_val = list_val
    """
    list_val child of reference_values
    """
