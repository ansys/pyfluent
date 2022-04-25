#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .coordinate_system import coordinate_system
from .direction_spec import direction_spec
from .direction_vector_components import direction_vector_components
from .e import e
from .flow_direction_component import flow_direction_component
from .geom_bgthread import geom_bgthread
from .geom_dir_spec import geom_dir_spec
from .geom_dir_x import geom_dir_x
from .geom_dir_y import geom_dir_y
from .geom_dir_z import geom_dir_z
from .geom_disable import geom_disable
from .geom_levels import geom_levels
from .hc import hc
from .heat_source import heat_source
from .intermit import intermit
from .k import k
from .ke_spec import ke_spec
from .kl import kl
from .ksgs import ksgs
from .ksgs_spec import ksgs_spec
from .mass_flow_multiplier import mass_flow_multiplier
from .nut import nut
from .o import o
from .phase_21 import phase
from .pid import pid
from .rst_spec import rst_spec
from .sgs_turb_intensity import sgs_turb_intensity
from .solar_fluxes import solar_fluxes
from .solar_shining_factor import solar_shining_factor
from .temperature_rise import temperature_rise
from .temperature_spec import temperature_spec
from .tinf import tinf
from .turb_hydraulic_diam import turb_hydraulic_diam
from .turb_intensity import turb_intensity
from .turb_length_scale import turb_length_scale
from .turb_viscosity_ratio import turb_viscosity_ratio
from .turb_viscosity_ratio_profile import turb_viscosity_ratio_profile
from .uu import uu
from .uv import uv
from .uw import uw
from .v2 import v2
from .vv import vv
from .vw import vw
from .ww import ww


class recirculation_inlet_child(Group):
    """'child_object_type' of recirculation_inlet."""

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
        "pid",
        "temperature_spec",
        "temperature_rise",
        "heat_source",
        "tinf",
        "hc",
        "direction_spec",
        "coordinate_system",
        "flow_direction_component",
        "direction_vector_components",
        "ke_spec",
        "nut",
        "kl",
        "intermit",
        "k",
        "e",
        "o",
        "v2",
        "turb_intensity",
        "turb_length_scale",
        "turb_hydraulic_diam",
        "turb_viscosity_ratio",
        "turb_viscosity_ratio_profile",
        "rst_spec",
        "uu",
        "vv",
        "ww",
        "uv",
        "vw",
        "uw",
        "ksgs_spec",
        "ksgs",
        "sgs_turb_intensity",
        "mass_flow_multiplier",
        "solar_fluxes",
        "solar_shining_factor",
    ]

    phase: phase = phase
    """
    phase child of recirculation_inlet_child
    """
    geom_disable: geom_disable = geom_disable
    """
    geom_disable child of recirculation_inlet_child
    """
    geom_dir_spec: geom_dir_spec = geom_dir_spec
    """
    geom_dir_spec child of recirculation_inlet_child
    """
    geom_dir_x: geom_dir_x = geom_dir_x
    """
    geom_dir_x child of recirculation_inlet_child
    """
    geom_dir_y: geom_dir_y = geom_dir_y
    """
    geom_dir_y child of recirculation_inlet_child
    """
    geom_dir_z: geom_dir_z = geom_dir_z
    """
    geom_dir_z child of recirculation_inlet_child
    """
    geom_levels: geom_levels = geom_levels
    """
    geom_levels child of recirculation_inlet_child
    """
    geom_bgthread: geom_bgthread = geom_bgthread
    """
    geom_bgthread child of recirculation_inlet_child
    """
    pid: pid = pid
    """
    pid child of recirculation_inlet_child
    """
    temperature_spec: temperature_spec = temperature_spec
    """
    temperature_spec child of recirculation_inlet_child
    """
    temperature_rise: temperature_rise = temperature_rise
    """
    temperature_rise child of recirculation_inlet_child
    """
    heat_source: heat_source = heat_source
    """
    heat_source child of recirculation_inlet_child
    """
    tinf: tinf = tinf
    """
    tinf child of recirculation_inlet_child
    """
    hc: hc = hc
    """
    hc child of recirculation_inlet_child
    """
    direction_spec: direction_spec = direction_spec
    """
    direction_spec child of recirculation_inlet_child
    """
    coordinate_system: coordinate_system = coordinate_system
    """
    coordinate_system child of recirculation_inlet_child
    """
    flow_direction_component: flow_direction_component = (
        flow_direction_component
    )
    """
    flow_direction_component child of recirculation_inlet_child
    """
    direction_vector_components: direction_vector_components = (
        direction_vector_components
    )
    """
    direction_vector_components child of recirculation_inlet_child
    """
    ke_spec: ke_spec = ke_spec
    """
    ke_spec child of recirculation_inlet_child
    """
    nut: nut = nut
    """
    nut child of recirculation_inlet_child
    """
    kl: kl = kl
    """
    kl child of recirculation_inlet_child
    """
    intermit: intermit = intermit
    """
    intermit child of recirculation_inlet_child
    """
    k: k = k
    """
    k child of recirculation_inlet_child
    """
    e: e = e
    """
    e child of recirculation_inlet_child
    """
    o: o = o
    """
    o child of recirculation_inlet_child
    """
    v2: v2 = v2
    """
    v2 child of recirculation_inlet_child
    """
    turb_intensity: turb_intensity = turb_intensity
    """
    turb_intensity child of recirculation_inlet_child
    """
    turb_length_scale: turb_length_scale = turb_length_scale
    """
    turb_length_scale child of recirculation_inlet_child
    """
    turb_hydraulic_diam: turb_hydraulic_diam = turb_hydraulic_diam
    """
    turb_hydraulic_diam child of recirculation_inlet_child
    """
    turb_viscosity_ratio: turb_viscosity_ratio = turb_viscosity_ratio
    """
    turb_viscosity_ratio child of recirculation_inlet_child
    """
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile = (
        turb_viscosity_ratio_profile
    )
    """
    turb_viscosity_ratio_profile child of recirculation_inlet_child
    """
    rst_spec: rst_spec = rst_spec
    """
    rst_spec child of recirculation_inlet_child
    """
    uu: uu = uu
    """
    uu child of recirculation_inlet_child
    """
    vv: vv = vv
    """
    vv child of recirculation_inlet_child
    """
    ww: ww = ww
    """
    ww child of recirculation_inlet_child
    """
    uv: uv = uv
    """
    uv child of recirculation_inlet_child
    """
    vw: vw = vw
    """
    vw child of recirculation_inlet_child
    """
    uw: uw = uw
    """
    uw child of recirculation_inlet_child
    """
    ksgs_spec: ksgs_spec = ksgs_spec
    """
    ksgs_spec child of recirculation_inlet_child
    """
    ksgs: ksgs = ksgs
    """
    ksgs child of recirculation_inlet_child
    """
    sgs_turb_intensity: sgs_turb_intensity = sgs_turb_intensity
    """
    sgs_turb_intensity child of recirculation_inlet_child
    """
    mass_flow_multiplier: mass_flow_multiplier = mass_flow_multiplier
    """
    mass_flow_multiplier child of recirculation_inlet_child
    """
    solar_fluxes: solar_fluxes = solar_fluxes
    """
    solar_fluxes child of recirculation_inlet_child
    """
    solar_shining_factor: solar_shining_factor = solar_shining_factor
    """
    solar_shining_factor child of recirculation_inlet_child
    """
