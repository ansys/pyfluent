#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .phase_16 import phase
from .geom_disable import geom_disable
from .geom_dir_spec import geom_dir_spec
from .geom_dir_x import geom_dir_x
from .geom_dir_y import geom_dir_y
from .geom_dir_z import geom_dir_z
from .geom_levels import geom_levels
from .geom_bgthread import geom_bgthread
from .p import p
from .m import m
from .t import t
from .non_equil_boundary import non_equil_boundary
from .tve import tve
from .coordinate_system import coordinate_system
from .ni_1 import ni
from .nj_1 import nj
from .nk_1 import nk
from .flow_direction_component import flow_direction_component
from .axis_direction_component_1 import axis_direction_component
from .axis_origin_component_1 import axis_origin_component
from .ke_spec import ke_spec
from .nut import nut
from .kl import kl
from .intermit import intermit
from .k import k
from .e import e
from .o import o
from .v2 import v2
from .turb_intensity import turb_intensity
from .turb_length_scale import turb_length_scale
from .turb_hydraulic_diam import turb_hydraulic_diam
from .turb_viscosity_ratio import turb_viscosity_ratio
from .turb_viscosity_ratio_profile import turb_viscosity_ratio_profile
from .rst_spec import rst_spec
from .uu import uu
from .vv import vv
from .ww import ww
from .uv import uv
from .vw import vw
from .uw import uw
from .ksgs_spec import ksgs_spec
from .ksgs import ksgs
from .sgs_turb_intensity import sgs_turb_intensity
from .radiation_bc import radiation_bc
from .radial_direction_component import radial_direction_component
from .coll_dtheta import coll_dtheta
from .coll_dphi import coll_dphi
from .band_q_irrad import band_q_irrad
from .band_q_irrad_diffuse import band_q_irrad_diffuse
from .parallel_collimated_beam import parallel_collimated_beam
from .solar_direction import solar_direction
from .solar_irradiation import solar_irradiation
from .t_b_b_spec import t_b_b_spec
from .t_b_b import t_b_b
from .in_emiss import in_emiss
from .fmean import fmean
from .fvar import fvar
from .fmean2 import fmean2
from .fvar2 import fvar2
from .species_in_mole_fractions import species_in_mole_fractions
from .mf import mf
from .elec_potential_type import elec_potential_type
from .potential_value import potential_value
from .dual_potential_type import dual_potential_type
from .dual_potential_value import dual_potential_value
from .x_displacement_type import x_displacement_type
from .x_displacement_value import x_displacement_value
from .y_displacement_type import y_displacement_type
from .y_displacement_value import y_displacement_value
from .z_displacement_type import z_displacement_type
from .z_displacement_value import z_displacement_value
from .prob_mode_1 import prob_mode_1
from .prob_mode_2 import prob_mode_2
from .prob_mode_3 import prob_mode_3
from .pollut_no import pollut_no
from .pollut_hcn import pollut_hcn
from .pollut_nh3 import pollut_nh3
from .pollut_n2o import pollut_n2o
from .pollut_urea import pollut_urea
from .pollut_hnco import pollut_hnco
from .pollut_nco import pollut_nco
from .pollut_so2 import pollut_so2
from .pollut_h2s import pollut_h2s
from .pollut_so3 import pollut_so3
from .pollut_sh import pollut_sh
from .pollut_so import pollut_so
from .pollut_soot import pollut_soot
from .pollut_nuclei import pollut_nuclei
from .pollut_ctar import pollut_ctar
from .pollut_hg import pollut_hg
from .pollut_hgcl2 import pollut_hgcl2
from .pollut_hcl import pollut_hcl
from .pollut_hgo import pollut_hgo
from .pollut_cl import pollut_cl
from .pollut_cl2 import pollut_cl2
from .pollut_hgcl import pollut_hgcl
from .pollut_hocl import pollut_hocl
from .fensapice_flow_bc_subtype import fensapice_flow_bc_subtype
from .fensapice_drop_bccustom import fensapice_drop_bccustom
from .fensapice_drop_lwc import fensapice_drop_lwc
from .fensapice_drop_dtemp import fensapice_drop_dtemp
from .fensapice_drop_ddiam import fensapice_drop_ddiam
from .fensapice_drop_dv import fensapice_drop_dv
from .fensapice_drop_dx import fensapice_drop_dx
from .fensapice_drop_dy import fensapice_drop_dy
from .fensapice_drop_dz import fensapice_drop_dz
from .fensapice_dpm_surface_injection import fensapice_dpm_surface_injection
from .fensapice_dpm_inj_nstream import fensapice_dpm_inj_nstream
from .fensapice_drop_icc import fensapice_drop_icc
from .fensapice_drop_ctemp import fensapice_drop_ctemp
from .fensapice_drop_cdiam import fensapice_drop_cdiam
from .fensapice_drop_cv import fensapice_drop_cv
from .fensapice_drop_cx import fensapice_drop_cx
from .fensapice_drop_cy import fensapice_drop_cy
from .fensapice_drop_cz import fensapice_drop_cz
from .fensapice_drop_vrh import fensapice_drop_vrh
from .fensapice_drop_vrh_1 import fensapice_drop_vrh_1
from .fensapice_drop_vc import fensapice_drop_vc
from .uds_bc import uds_bc
from .uds import uds
from .dpm_bc_type import dpm_bc_type
from .dpm_bc_collision_partner import dpm_bc_collision_partner
from .reinj_inj import reinj_inj
from .dpm_bc_udf import dpm_bc_udf
from .solar_fluxes import solar_fluxes
from .solar_shining_factor import solar_shining_factor
from .radiating_s2s_surface import radiating_s2s_surface
class pressure_far_field_child(Group):
    """
    'child_object_type' of pressure_far_field
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'p', 'm', 't',
         'non_equil_boundary', 'tve', 'coordinate_system', 'ni', 'nj', 'nk',
         'flow_direction_component', 'axis_direction_component',
         'axis_origin_component', 'ke_spec', 'nut', 'kl', 'intermit', 'k',
         'e', 'o', 'v2', 'turb_intensity', 'turb_length_scale',
         'turb_hydraulic_diam', 'turb_viscosity_ratio',
         'turb_viscosity_ratio_profile', 'rst_spec', 'uu', 'vv', 'ww', 'uv',
         'vw', 'uw', 'ksgs_spec', 'ksgs', 'sgs_turb_intensity',
         'radiation_bc', 'radial_direction_component', 'coll_dtheta',
         'coll_dphi', 'band_q_irrad', 'band_q_irrad_diffuse',
         'parallel_collimated_beam', 'solar_direction', 'solar_irradiation',
         't_b_b_spec', 't_b_b', 'in_emiss', 'fmean', 'fvar', 'fmean2',
         'fvar2', 'species_in_mole_fractions', 'mf', 'elec_potential_type',
         'potential_value', 'dual_potential_type', 'dual_potential_value',
         'x_displacement_type', 'x_displacement_value', 'y_displacement_type',
         'y_displacement_value', 'z_displacement_type',
         'z_displacement_value', 'prob_mode_1', 'prob_mode_2', 'prob_mode_3',
         'pollut_no', 'pollut_hcn', 'pollut_nh3', 'pollut_n2o', 'pollut_urea',
         'pollut_hnco', 'pollut_nco', 'pollut_so2', 'pollut_h2s',
         'pollut_so3', 'pollut_sh', 'pollut_so', 'pollut_soot',
         'pollut_nuclei', 'pollut_ctar', 'pollut_hg', 'pollut_hgcl2',
         'pollut_hcl', 'pollut_hgo', 'pollut_cl', 'pollut_cl2', 'pollut_hgcl',
         'pollut_hocl', 'fensapice_flow_bc_subtype',
         'fensapice_drop_bccustom', 'fensapice_drop_lwc',
         'fensapice_drop_dtemp', 'fensapice_drop_ddiam', 'fensapice_drop_dv',
         'fensapice_drop_dx', 'fensapice_drop_dy', 'fensapice_drop_dz',
         'fensapice_dpm_surface_injection', 'fensapice_dpm_inj_nstream',
         'fensapice_drop_icc', 'fensapice_drop_ctemp', 'fensapice_drop_cdiam',
         'fensapice_drop_cv', 'fensapice_drop_cx', 'fensapice_drop_cy',
         'fensapice_drop_cz', 'fensapice_drop_vrh', 'fensapice_drop_vrh_1',
         'fensapice_drop_vc', 'uds_bc', 'uds', 'dpm_bc_type',
         'dpm_bc_collision_partner', 'reinj_inj', 'dpm_bc_udf',
         'solar_fluxes', 'solar_shining_factor', 'radiating_s2s_surface']

    phase: phase = phase
    """
    phase child of pressure_far_field_child
    """
    geom_disable: geom_disable = geom_disable
    """
    geom_disable child of pressure_far_field_child
    """
    geom_dir_spec: geom_dir_spec = geom_dir_spec
    """
    geom_dir_spec child of pressure_far_field_child
    """
    geom_dir_x: geom_dir_x = geom_dir_x
    """
    geom_dir_x child of pressure_far_field_child
    """
    geom_dir_y: geom_dir_y = geom_dir_y
    """
    geom_dir_y child of pressure_far_field_child
    """
    geom_dir_z: geom_dir_z = geom_dir_z
    """
    geom_dir_z child of pressure_far_field_child
    """
    geom_levels: geom_levels = geom_levels
    """
    geom_levels child of pressure_far_field_child
    """
    geom_bgthread: geom_bgthread = geom_bgthread
    """
    geom_bgthread child of pressure_far_field_child
    """
    p: p = p
    """
    p child of pressure_far_field_child
    """
    m: m = m
    """
    m child of pressure_far_field_child
    """
    t: t = t
    """
    t child of pressure_far_field_child
    """
    non_equil_boundary: non_equil_boundary = non_equil_boundary
    """
    non_equil_boundary child of pressure_far_field_child
    """
    tve: tve = tve
    """
    tve child of pressure_far_field_child
    """
    coordinate_system: coordinate_system = coordinate_system
    """
    coordinate_system child of pressure_far_field_child
    """
    ni: ni = ni
    """
    ni child of pressure_far_field_child
    """
    nj: nj = nj
    """
    nj child of pressure_far_field_child
    """
    nk: nk = nk
    """
    nk child of pressure_far_field_child
    """
    flow_direction_component: flow_direction_component = flow_direction_component
    """
    flow_direction_component child of pressure_far_field_child
    """
    axis_direction_component: axis_direction_component = axis_direction_component
    """
    axis_direction_component child of pressure_far_field_child
    """
    axis_origin_component: axis_origin_component = axis_origin_component
    """
    axis_origin_component child of pressure_far_field_child
    """
    ke_spec: ke_spec = ke_spec
    """
    ke_spec child of pressure_far_field_child
    """
    nut: nut = nut
    """
    nut child of pressure_far_field_child
    """
    kl: kl = kl
    """
    kl child of pressure_far_field_child
    """
    intermit: intermit = intermit
    """
    intermit child of pressure_far_field_child
    """
    k: k = k
    """
    k child of pressure_far_field_child
    """
    e: e = e
    """
    e child of pressure_far_field_child
    """
    o: o = o
    """
    o child of pressure_far_field_child
    """
    v2: v2 = v2
    """
    v2 child of pressure_far_field_child
    """
    turb_intensity: turb_intensity = turb_intensity
    """
    turb_intensity child of pressure_far_field_child
    """
    turb_length_scale: turb_length_scale = turb_length_scale
    """
    turb_length_scale child of pressure_far_field_child
    """
    turb_hydraulic_diam: turb_hydraulic_diam = turb_hydraulic_diam
    """
    turb_hydraulic_diam child of pressure_far_field_child
    """
    turb_viscosity_ratio: turb_viscosity_ratio = turb_viscosity_ratio
    """
    turb_viscosity_ratio child of pressure_far_field_child
    """
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile = turb_viscosity_ratio_profile
    """
    turb_viscosity_ratio_profile child of pressure_far_field_child
    """
    rst_spec: rst_spec = rst_spec
    """
    rst_spec child of pressure_far_field_child
    """
    uu: uu = uu
    """
    uu child of pressure_far_field_child
    """
    vv: vv = vv
    """
    vv child of pressure_far_field_child
    """
    ww: ww = ww
    """
    ww child of pressure_far_field_child
    """
    uv: uv = uv
    """
    uv child of pressure_far_field_child
    """
    vw: vw = vw
    """
    vw child of pressure_far_field_child
    """
    uw: uw = uw
    """
    uw child of pressure_far_field_child
    """
    ksgs_spec: ksgs_spec = ksgs_spec
    """
    ksgs_spec child of pressure_far_field_child
    """
    ksgs: ksgs = ksgs
    """
    ksgs child of pressure_far_field_child
    """
    sgs_turb_intensity: sgs_turb_intensity = sgs_turb_intensity
    """
    sgs_turb_intensity child of pressure_far_field_child
    """
    radiation_bc: radiation_bc = radiation_bc
    """
    radiation_bc child of pressure_far_field_child
    """
    radial_direction_component: radial_direction_component = radial_direction_component
    """
    radial_direction_component child of pressure_far_field_child
    """
    coll_dtheta: coll_dtheta = coll_dtheta
    """
    coll_dtheta child of pressure_far_field_child
    """
    coll_dphi: coll_dphi = coll_dphi
    """
    coll_dphi child of pressure_far_field_child
    """
    band_q_irrad: band_q_irrad = band_q_irrad
    """
    band_q_irrad child of pressure_far_field_child
    """
    band_q_irrad_diffuse: band_q_irrad_diffuse = band_q_irrad_diffuse
    """
    band_q_irrad_diffuse child of pressure_far_field_child
    """
    parallel_collimated_beam: parallel_collimated_beam = parallel_collimated_beam
    """
    parallel_collimated_beam child of pressure_far_field_child
    """
    solar_direction: solar_direction = solar_direction
    """
    solar_direction child of pressure_far_field_child
    """
    solar_irradiation: solar_irradiation = solar_irradiation
    """
    solar_irradiation child of pressure_far_field_child
    """
    t_b_b_spec: t_b_b_spec = t_b_b_spec
    """
    t_b_b_spec child of pressure_far_field_child
    """
    t_b_b: t_b_b = t_b_b
    """
    t_b_b child of pressure_far_field_child
    """
    in_emiss: in_emiss = in_emiss
    """
    in_emiss child of pressure_far_field_child
    """
    fmean: fmean = fmean
    """
    fmean child of pressure_far_field_child
    """
    fvar: fvar = fvar
    """
    fvar child of pressure_far_field_child
    """
    fmean2: fmean2 = fmean2
    """
    fmean2 child of pressure_far_field_child
    """
    fvar2: fvar2 = fvar2
    """
    fvar2 child of pressure_far_field_child
    """
    species_in_mole_fractions: species_in_mole_fractions = species_in_mole_fractions
    """
    species_in_mole_fractions child of pressure_far_field_child
    """
    mf: mf = mf
    """
    mf child of pressure_far_field_child
    """
    elec_potential_type: elec_potential_type = elec_potential_type
    """
    elec_potential_type child of pressure_far_field_child
    """
    potential_value: potential_value = potential_value
    """
    potential_value child of pressure_far_field_child
    """
    dual_potential_type: dual_potential_type = dual_potential_type
    """
    dual_potential_type child of pressure_far_field_child
    """
    dual_potential_value: dual_potential_value = dual_potential_value
    """
    dual_potential_value child of pressure_far_field_child
    """
    x_displacement_type: x_displacement_type = x_displacement_type
    """
    x_displacement_type child of pressure_far_field_child
    """
    x_displacement_value: x_displacement_value = x_displacement_value
    """
    x_displacement_value child of pressure_far_field_child
    """
    y_displacement_type: y_displacement_type = y_displacement_type
    """
    y_displacement_type child of pressure_far_field_child
    """
    y_displacement_value: y_displacement_value = y_displacement_value
    """
    y_displacement_value child of pressure_far_field_child
    """
    z_displacement_type: z_displacement_type = z_displacement_type
    """
    z_displacement_type child of pressure_far_field_child
    """
    z_displacement_value: z_displacement_value = z_displacement_value
    """
    z_displacement_value child of pressure_far_field_child
    """
    prob_mode_1: prob_mode_1 = prob_mode_1
    """
    prob_mode_1 child of pressure_far_field_child
    """
    prob_mode_2: prob_mode_2 = prob_mode_2
    """
    prob_mode_2 child of pressure_far_field_child
    """
    prob_mode_3: prob_mode_3 = prob_mode_3
    """
    prob_mode_3 child of pressure_far_field_child
    """
    pollut_no: pollut_no = pollut_no
    """
    pollut_no child of pressure_far_field_child
    """
    pollut_hcn: pollut_hcn = pollut_hcn
    """
    pollut_hcn child of pressure_far_field_child
    """
    pollut_nh3: pollut_nh3 = pollut_nh3
    """
    pollut_nh3 child of pressure_far_field_child
    """
    pollut_n2o: pollut_n2o = pollut_n2o
    """
    pollut_n2o child of pressure_far_field_child
    """
    pollut_urea: pollut_urea = pollut_urea
    """
    pollut_urea child of pressure_far_field_child
    """
    pollut_hnco: pollut_hnco = pollut_hnco
    """
    pollut_hnco child of pressure_far_field_child
    """
    pollut_nco: pollut_nco = pollut_nco
    """
    pollut_nco child of pressure_far_field_child
    """
    pollut_so2: pollut_so2 = pollut_so2
    """
    pollut_so2 child of pressure_far_field_child
    """
    pollut_h2s: pollut_h2s = pollut_h2s
    """
    pollut_h2s child of pressure_far_field_child
    """
    pollut_so3: pollut_so3 = pollut_so3
    """
    pollut_so3 child of pressure_far_field_child
    """
    pollut_sh: pollut_sh = pollut_sh
    """
    pollut_sh child of pressure_far_field_child
    """
    pollut_so: pollut_so = pollut_so
    """
    pollut_so child of pressure_far_field_child
    """
    pollut_soot: pollut_soot = pollut_soot
    """
    pollut_soot child of pressure_far_field_child
    """
    pollut_nuclei: pollut_nuclei = pollut_nuclei
    """
    pollut_nuclei child of pressure_far_field_child
    """
    pollut_ctar: pollut_ctar = pollut_ctar
    """
    pollut_ctar child of pressure_far_field_child
    """
    pollut_hg: pollut_hg = pollut_hg
    """
    pollut_hg child of pressure_far_field_child
    """
    pollut_hgcl2: pollut_hgcl2 = pollut_hgcl2
    """
    pollut_hgcl2 child of pressure_far_field_child
    """
    pollut_hcl: pollut_hcl = pollut_hcl
    """
    pollut_hcl child of pressure_far_field_child
    """
    pollut_hgo: pollut_hgo = pollut_hgo
    """
    pollut_hgo child of pressure_far_field_child
    """
    pollut_cl: pollut_cl = pollut_cl
    """
    pollut_cl child of pressure_far_field_child
    """
    pollut_cl2: pollut_cl2 = pollut_cl2
    """
    pollut_cl2 child of pressure_far_field_child
    """
    pollut_hgcl: pollut_hgcl = pollut_hgcl
    """
    pollut_hgcl child of pressure_far_field_child
    """
    pollut_hocl: pollut_hocl = pollut_hocl
    """
    pollut_hocl child of pressure_far_field_child
    """
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype = fensapice_flow_bc_subtype
    """
    fensapice_flow_bc_subtype child of pressure_far_field_child
    """
    fensapice_drop_bccustom: fensapice_drop_bccustom = fensapice_drop_bccustom
    """
    fensapice_drop_bccustom child of pressure_far_field_child
    """
    fensapice_drop_lwc: fensapice_drop_lwc = fensapice_drop_lwc
    """
    fensapice_drop_lwc child of pressure_far_field_child
    """
    fensapice_drop_dtemp: fensapice_drop_dtemp = fensapice_drop_dtemp
    """
    fensapice_drop_dtemp child of pressure_far_field_child
    """
    fensapice_drop_ddiam: fensapice_drop_ddiam = fensapice_drop_ddiam
    """
    fensapice_drop_ddiam child of pressure_far_field_child
    """
    fensapice_drop_dv: fensapice_drop_dv = fensapice_drop_dv
    """
    fensapice_drop_dv child of pressure_far_field_child
    """
    fensapice_drop_dx: fensapice_drop_dx = fensapice_drop_dx
    """
    fensapice_drop_dx child of pressure_far_field_child
    """
    fensapice_drop_dy: fensapice_drop_dy = fensapice_drop_dy
    """
    fensapice_drop_dy child of pressure_far_field_child
    """
    fensapice_drop_dz: fensapice_drop_dz = fensapice_drop_dz
    """
    fensapice_drop_dz child of pressure_far_field_child
    """
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection = fensapice_dpm_surface_injection
    """
    fensapice_dpm_surface_injection child of pressure_far_field_child
    """
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream = fensapice_dpm_inj_nstream
    """
    fensapice_dpm_inj_nstream child of pressure_far_field_child
    """
    fensapice_drop_icc: fensapice_drop_icc = fensapice_drop_icc
    """
    fensapice_drop_icc child of pressure_far_field_child
    """
    fensapice_drop_ctemp: fensapice_drop_ctemp = fensapice_drop_ctemp
    """
    fensapice_drop_ctemp child of pressure_far_field_child
    """
    fensapice_drop_cdiam: fensapice_drop_cdiam = fensapice_drop_cdiam
    """
    fensapice_drop_cdiam child of pressure_far_field_child
    """
    fensapice_drop_cv: fensapice_drop_cv = fensapice_drop_cv
    """
    fensapice_drop_cv child of pressure_far_field_child
    """
    fensapice_drop_cx: fensapice_drop_cx = fensapice_drop_cx
    """
    fensapice_drop_cx child of pressure_far_field_child
    """
    fensapice_drop_cy: fensapice_drop_cy = fensapice_drop_cy
    """
    fensapice_drop_cy child of pressure_far_field_child
    """
    fensapice_drop_cz: fensapice_drop_cz = fensapice_drop_cz
    """
    fensapice_drop_cz child of pressure_far_field_child
    """
    fensapice_drop_vrh: fensapice_drop_vrh = fensapice_drop_vrh
    """
    fensapice_drop_vrh child of pressure_far_field_child
    """
    fensapice_drop_vrh_1: fensapice_drop_vrh_1 = fensapice_drop_vrh_1
    """
    fensapice_drop_vrh_1 child of pressure_far_field_child
    """
    fensapice_drop_vc: fensapice_drop_vc = fensapice_drop_vc
    """
    fensapice_drop_vc child of pressure_far_field_child
    """
    uds_bc: uds_bc = uds_bc
    """
    uds_bc child of pressure_far_field_child
    """
    uds: uds = uds
    """
    uds child of pressure_far_field_child
    """
    dpm_bc_type: dpm_bc_type = dpm_bc_type
    """
    dpm_bc_type child of pressure_far_field_child
    """
    dpm_bc_collision_partner: dpm_bc_collision_partner = dpm_bc_collision_partner
    """
    dpm_bc_collision_partner child of pressure_far_field_child
    """
    reinj_inj: reinj_inj = reinj_inj
    """
    reinj_inj child of pressure_far_field_child
    """
    dpm_bc_udf: dpm_bc_udf = dpm_bc_udf
    """
    dpm_bc_udf child of pressure_far_field_child
    """
    solar_fluxes: solar_fluxes = solar_fluxes
    """
    solar_fluxes child of pressure_far_field_child
    """
    solar_shining_factor: solar_shining_factor = solar_shining_factor
    """
    solar_shining_factor child of pressure_far_field_child
    """
    radiating_s2s_surface: radiating_s2s_surface = radiating_s2s_surface
    """
    radiating_s2s_surface child of pressure_far_field_child
    """
