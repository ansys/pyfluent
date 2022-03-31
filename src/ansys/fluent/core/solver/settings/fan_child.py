#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .average_dp import average_dp
from .axis_direction_component_1 import axis_direction_component
from .axis_origin_component_1 import axis_origin_component
from .c import c
from .dir import dir
from .dp_profile import dp_profile
from .dpm_bc_collision_partner import dpm_bc_collision_partner
from .dpm_bc_type import dpm_bc_type
from .dpm_bc_udf import dpm_bc_udf
from .fan_vr import fan_vr
from .fr import fr
from .geom_bgthread import geom_bgthread
from .geom_dir_spec import geom_dir_spec
from .geom_dir_x import geom_dir_x
from .geom_dir_y import geom_dir_y
from .geom_dir_z import geom_dir_z
from .geom_disable import geom_disable
from .geom_levels import geom_levels
from .hub import hub
from .limit_range import limit_range
from .new_fan_definition import new_fan_definition
from .phase_4 import phase
from .porous_jump_turb_wall_treatment import porous_jump_turb_wall_treatment
from .profile_dp import profile_dp
from .profile_vr import profile_vr
from .profile_vt import profile_vt
from .reinj_inj import reinj_inj
from .strength import strength
from .swirl_factor import swirl_factor
from .swirl_model import swirl_model
from .v_max import v_max
from .v_min import v_min
from .vr_profile import vr_profile
from .vt_profile import vt_profile


class fan_child(Group):
    """'child_object_type' of fan."""

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
        "porous_jump_turb_wall_treatment",
        "dir",
        "average_dp",
        "c",
        "limit_range",
        "v_min",
        "v_max",
        "strength",
        "profile_dp",
        "dp_profile",
        "swirl_model",
        "fan_vr",
        "fr",
        "hub",
        "axis_origin_component",
        "axis_direction_component",
        "profile_vt",
        "vt_profile",
        "profile_vr",
        "vr_profile",
        "swirl_factor",
        "dpm_bc_type",
        "dpm_bc_collision_partner",
        "reinj_inj",
        "dpm_bc_udf",
        "new_fan_definition",
    ]

    phase: phase = phase
    """
    phase child of fan_child
    """
    geom_disable: geom_disable = geom_disable
    """
    geom_disable child of fan_child
    """
    geom_dir_spec: geom_dir_spec = geom_dir_spec
    """
    geom_dir_spec child of fan_child
    """
    geom_dir_x: geom_dir_x = geom_dir_x
    """
    geom_dir_x child of fan_child
    """
    geom_dir_y: geom_dir_y = geom_dir_y
    """
    geom_dir_y child of fan_child
    """
    geom_dir_z: geom_dir_z = geom_dir_z
    """
    geom_dir_z child of fan_child
    """
    geom_levels: geom_levels = geom_levels
    """
    geom_levels child of fan_child
    """
    geom_bgthread: geom_bgthread = geom_bgthread
    """
    geom_bgthread child of fan_child
    """
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment = (
        porous_jump_turb_wall_treatment
    )
    """
    porous_jump_turb_wall_treatment child of fan_child
    """
    dir: dir = dir
    """
    dir child of fan_child
    """
    average_dp: average_dp = average_dp
    """
    average_dp child of fan_child
    """
    c: c = c
    """
    c child of fan_child
    """
    limit_range: limit_range = limit_range
    """
    limit_range child of fan_child
    """
    v_min: v_min = v_min
    """
    v_min child of fan_child
    """
    v_max: v_max = v_max
    """
    v_max child of fan_child
    """
    strength: strength = strength
    """
    strength child of fan_child
    """
    profile_dp: profile_dp = profile_dp
    """
    profile_dp child of fan_child
    """
    dp_profile: dp_profile = dp_profile
    """
    dp_profile child of fan_child
    """
    swirl_model: swirl_model = swirl_model
    """
    swirl_model child of fan_child
    """
    fan_vr: fan_vr = fan_vr
    """
    fan_vr child of fan_child
    """
    fr: fr = fr
    """
    fr child of fan_child
    """
    hub: hub = hub
    """
    hub child of fan_child
    """
    axis_origin_component: axis_origin_component = axis_origin_component
    """
    axis_origin_component child of fan_child
    """
    axis_direction_component: axis_direction_component = (
        axis_direction_component
    )
    """
    axis_direction_component child of fan_child
    """
    profile_vt: profile_vt = profile_vt
    """
    profile_vt child of fan_child
    """
    vt_profile: vt_profile = vt_profile
    """
    vt_profile child of fan_child
    """
    profile_vr: profile_vr = profile_vr
    """
    profile_vr child of fan_child
    """
    vr_profile: vr_profile = vr_profile
    """
    vr_profile child of fan_child
    """
    swirl_factor: swirl_factor = swirl_factor
    """
    swirl_factor child of fan_child
    """
    dpm_bc_type: dpm_bc_type = dpm_bc_type
    """
    dpm_bc_type child of fan_child
    """
    dpm_bc_collision_partner: dpm_bc_collision_partner = (
        dpm_bc_collision_partner
    )
    """
    dpm_bc_collision_partner child of fan_child
    """
    reinj_inj: reinj_inj = reinj_inj
    """
    reinj_inj child of fan_child
    """
    dpm_bc_udf: dpm_bc_udf = dpm_bc_udf
    """
    dpm_bc_udf child of fan_child
    """
    new_fan_definition: new_fan_definition = new_fan_definition
    """
    new_fan_definition child of fan_child
    """
