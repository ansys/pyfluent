#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .band_q_irrad import band_q_irrad
from .band_q_irrad_diffuse import band_q_irrad_diffuse
from .coll_dphi import coll_dphi
from .coll_dtheta import coll_dtheta
from .dpm_bc_collision_partner import dpm_bc_collision_partner
from .dpm_bc_type import dpm_bc_type
from .dpm_bc_udf import dpm_bc_udf
from .dual_potential_type import dual_potential_type
from .dual_potential_value import dual_potential_value
from .elec_potential_type import elec_potential_type
from .flowrate_frac import flowrate_frac
from .geom_bgthread import geom_bgthread
from .geom_dir_spec import geom_dir_spec
from .geom_dir_x import geom_dir_x
from .geom_dir_y import geom_dir_y
from .geom_dir_z import geom_dir_z
from .geom_disable import geom_disable
from .geom_levels import geom_levels
from .in_emiss import in_emiss
from .parallel_collimated_beam import parallel_collimated_beam
from .potential_value import potential_value
from .radiating_s2s_surface import radiating_s2s_surface
from .radiation_bc import radiation_bc
from .reinj_inj import reinj_inj
from .solar_direction import solar_direction
from .solar_fluxes import solar_fluxes
from .solar_irradiation import solar_irradiation
from .solar_shining_factor import solar_shining_factor
from .t_b_b import t_b_b
from .t_b_b_spec import t_b_b_spec
from .uds import uds
from .uds_bc import uds_bc
from .x_displacement_type import x_displacement_type
from .x_displacement_value import x_displacement_value
from .y_displacement_type import y_displacement_type
from .y_displacement_value import y_displacement_value
from .z_displacement_type import z_displacement_type
from .z_displacement_value import z_displacement_value


class phase_child(Group):
    """'child_object_type' of phase."""

    fluent_name = "child-object-type"

    child_names = [
        "geom_disable",
        "geom_dir_spec",
        "geom_dir_x",
        "geom_dir_y",
        "geom_dir_z",
        "geom_levels",
        "geom_bgthread",
        "flowrate_frac",
        "elec_potential_type",
        "potential_value",
        "dual_potential_type",
        "dual_potential_value",
        "x_displacement_type",
        "x_displacement_value",
        "y_displacement_type",
        "y_displacement_value",
        "z_displacement_type",
        "z_displacement_value",
        "uds_bc",
        "uds",
        "radiation_bc",
        "coll_dtheta",
        "coll_dphi",
        "band_q_irrad",
        "band_q_irrad_diffuse",
        "parallel_collimated_beam",
        "solar_direction",
        "solar_irradiation",
        "t_b_b_spec",
        "t_b_b",
        "in_emiss",
        "dpm_bc_type",
        "dpm_bc_collision_partner",
        "reinj_inj",
        "dpm_bc_udf",
        "solar_fluxes",
        "solar_shining_factor",
        "radiating_s2s_surface",
    ]

    geom_disable: geom_disable = geom_disable
    """
    geom_disable child of phase_child
    """
    geom_dir_spec: geom_dir_spec = geom_dir_spec
    """
    geom_dir_spec child of phase_child
    """
    geom_dir_x: geom_dir_x = geom_dir_x
    """
    geom_dir_x child of phase_child
    """
    geom_dir_y: geom_dir_y = geom_dir_y
    """
    geom_dir_y child of phase_child
    """
    geom_dir_z: geom_dir_z = geom_dir_z
    """
    geom_dir_z child of phase_child
    """
    geom_levels: geom_levels = geom_levels
    """
    geom_levels child of phase_child
    """
    geom_bgthread: geom_bgthread = geom_bgthread
    """
    geom_bgthread child of phase_child
    """
    flowrate_frac: flowrate_frac = flowrate_frac
    """
    flowrate_frac child of phase_child
    """
    elec_potential_type: elec_potential_type = elec_potential_type
    """
    elec_potential_type child of phase_child
    """
    potential_value: potential_value = potential_value
    """
    potential_value child of phase_child
    """
    dual_potential_type: dual_potential_type = dual_potential_type
    """
    dual_potential_type child of phase_child
    """
    dual_potential_value: dual_potential_value = dual_potential_value
    """
    dual_potential_value child of phase_child
    """
    x_displacement_type: x_displacement_type = x_displacement_type
    """
    x_displacement_type child of phase_child
    """
    x_displacement_value: x_displacement_value = x_displacement_value
    """
    x_displacement_value child of phase_child
    """
    y_displacement_type: y_displacement_type = y_displacement_type
    """
    y_displacement_type child of phase_child
    """
    y_displacement_value: y_displacement_value = y_displacement_value
    """
    y_displacement_value child of phase_child
    """
    z_displacement_type: z_displacement_type = z_displacement_type
    """
    z_displacement_type child of phase_child
    """
    z_displacement_value: z_displacement_value = z_displacement_value
    """
    z_displacement_value child of phase_child
    """
    uds_bc: uds_bc = uds_bc
    """
    uds_bc child of phase_child
    """
    uds: uds = uds
    """
    uds child of phase_child
    """
    radiation_bc: radiation_bc = radiation_bc
    """
    radiation_bc child of phase_child
    """
    coll_dtheta: coll_dtheta = coll_dtheta
    """
    coll_dtheta child of phase_child
    """
    coll_dphi: coll_dphi = coll_dphi
    """
    coll_dphi child of phase_child
    """
    band_q_irrad: band_q_irrad = band_q_irrad
    """
    band_q_irrad child of phase_child
    """
    band_q_irrad_diffuse: band_q_irrad_diffuse = band_q_irrad_diffuse
    """
    band_q_irrad_diffuse child of phase_child
    """
    parallel_collimated_beam: parallel_collimated_beam = (
        parallel_collimated_beam
    )
    """
    parallel_collimated_beam child of phase_child
    """
    solar_direction: solar_direction = solar_direction
    """
    solar_direction child of phase_child
    """
    solar_irradiation: solar_irradiation = solar_irradiation
    """
    solar_irradiation child of phase_child
    """
    t_b_b_spec: t_b_b_spec = t_b_b_spec
    """
    t_b_b_spec child of phase_child
    """
    t_b_b: t_b_b = t_b_b
    """
    t_b_b child of phase_child
    """
    in_emiss: in_emiss = in_emiss
    """
    in_emiss child of phase_child
    """
    dpm_bc_type: dpm_bc_type = dpm_bc_type
    """
    dpm_bc_type child of phase_child
    """
    dpm_bc_collision_partner: dpm_bc_collision_partner = (
        dpm_bc_collision_partner
    )
    """
    dpm_bc_collision_partner child of phase_child
    """
    reinj_inj: reinj_inj = reinj_inj
    """
    reinj_inj child of phase_child
    """
    dpm_bc_udf: dpm_bc_udf = dpm_bc_udf
    """
    dpm_bc_udf child of phase_child
    """
    solar_fluxes: solar_fluxes = solar_fluxes
    """
    solar_fluxes child of phase_child
    """
    solar_shining_factor: solar_shining_factor = solar_shining_factor
    """
    solar_shining_factor child of phase_child
    """
    radiating_s2s_surface: radiating_s2s_surface = radiating_s2s_surface
    """
    radiating_s2s_surface child of phase_child
    """
