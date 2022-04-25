#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .flow_spec import flow_spec
from .geom_bgthread import geom_bgthread
from .geom_dir_spec import geom_dir_spec
from .geom_dir_x import geom_dir_x
from .geom_dir_y import geom_dir_y
from .geom_dir_z import geom_dir_z
from .geom_disable import geom_disable
from .geom_levels import geom_levels
from .mass_flow import mass_flow
from .mass_flux import mass_flux
from .phase_22 import phase
from .solar_fluxes import solar_fluxes
from .solar_shining_factor import solar_shining_factor


class recirculation_outlet_child(Group):
    """'child_object_type' of recirculation_outlet."""

    fluent_name = "child-object-type"

    child_names = [
        "phase",
        "geom_disable",
        "geom_dir_spec",
        "geom_dir_x",
        "geom_dir_y",
        "geom_dir_z",
        "geom_levels",
        "geom_bgthread",
        "flow_spec",
        "mass_flow",
        "mass_flux",
        "solar_fluxes",
        "solar_shining_factor",
    ]

    phase: phase = phase
    """
    phase child of recirculation_outlet_child
    """
    geom_disable: geom_disable = geom_disable
    """
    geom_disable child of recirculation_outlet_child
    """
    geom_dir_spec: geom_dir_spec = geom_dir_spec
    """
    geom_dir_spec child of recirculation_outlet_child
    """
    geom_dir_x: geom_dir_x = geom_dir_x
    """
    geom_dir_x child of recirculation_outlet_child
    """
    geom_dir_y: geom_dir_y = geom_dir_y
    """
    geom_dir_y child of recirculation_outlet_child
    """
    geom_dir_z: geom_dir_z = geom_dir_z
    """
    geom_dir_z child of recirculation_outlet_child
    """
    geom_levels: geom_levels = geom_levels
    """
    geom_levels child of recirculation_outlet_child
    """
    geom_bgthread: geom_bgthread = geom_bgthread
    """
    geom_bgthread child of recirculation_outlet_child
    """
    flow_spec: flow_spec = flow_spec
    """
    flow_spec child of recirculation_outlet_child
    """
    mass_flow: mass_flow = mass_flow
    """
    mass_flow child of recirculation_outlet_child
    """
    mass_flux: mass_flux = mass_flux
    """
    mass_flux child of recirculation_outlet_child
    """
    solar_fluxes: solar_fluxes = solar_fluxes
    """
    solar_fluxes child of recirculation_outlet_child
    """
    solar_shining_factor: solar_shining_factor = solar_shining_factor
    """
    solar_shining_factor child of recirculation_outlet_child
    """
