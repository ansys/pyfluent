#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .phase_18 import phase
from .geom_disable import geom_disable
from .geom_dir_spec import geom_dir_spec
from .geom_dir_x import geom_dir_x
from .geom_dir_y import geom_dir_y
from .geom_dir_z import geom_dir_z
from .geom_levels import geom_levels
from .geom_bgthread import geom_bgthread
from .open_channel import open_channel
from .outlet_number import outlet_number
from .pressure_spec_method import pressure_spec_method
from .press_spec import press_spec
from .frame_of_reference import frame_of_reference
from .phase_spec import phase_spec
from .ht_local import ht_local
from .p import p
from .p_profile_multiplier import p_profile_multiplier
from .ht_bottom import ht_bottom
from .den_spec import den_spec
from .t0 import t0
from .direction_spec import direction_spec
from .coordinate_system import coordinate_system
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
from .fmean2 import fmean2
from .fvar import fvar
from .fvar2 import fvar2
from .granular_temperature import granular_temperature
from .iac import iac
from .lsfun import lsfun
from .vof_spec import vof_spec
from .volume_fraction import volume_fraction
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
from .premixc import premixc
from .premixc_var import premixc_var
from .ecfm_sigma import ecfm_sigma
from .inert import inert
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
from .tss_scalar import tss_scalar
from .fensapice_flow_bc_subtype import fensapice_flow_bc_subtype
from .uds_bc import uds_bc
from .uds import uds
from .pb_disc_bc import pb_disc_bc
from .pb_disc import pb_disc
from .pb_qmom_bc import pb_qmom_bc
from .pb_qmom import pb_qmom
from .pb_smm_bc import pb_smm_bc
from .pb_smm import pb_smm
from .pb_dqmom_bc import pb_dqmom_bc
from .pb_dqmom import pb_dqmom
from .dpm_bc_type import dpm_bc_type
from .dpm_bc_collision_partner import dpm_bc_collision_partner
from .reinj_inj import reinj_inj
from .dpm_bc_udf import dpm_bc_udf
from .mixing_plane_thread import mixing_plane_thread
from .ac_options import ac_options
from .p_backflow_spec import p_backflow_spec
from .p_backflow_spec_gen import p_backflow_spec_gen
from .impedance_0 import impedance_0
from .impedance_1 import impedance_1
from .impedance_2 import impedance_2
from .ac_wave import ac_wave
from .prevent_reverse_flow import prevent_reverse_flow
from .radial import radial
from .avg_press_spec import avg_press_spec
from .press_averaging_method import press_averaging_method
from .targeted_mf_boundary import targeted_mf_boundary
from .targeted_mf import targeted_mf
from .targeted_mf_pmax import targeted_mf_pmax
from .targeted_mf_pmin import targeted_mf_pmin
from .gen_nrbc_spec import gen_nrbc_spec
from .wsf import wsf
from .wsb import wsb
from .wsn import wsn
from .solar_fluxes import solar_fluxes
from .solar_shining_factor import solar_shining_factor
from .radiating_s2s_surface import radiating_s2s_surface
class pressure_outlet_child(Group):
    """
    'child_object_type' of pressure_outlet
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'open_channel',
         'outlet_number', 'pressure_spec_method', 'press_spec',
         'frame_of_reference', 'phase_spec', 'ht_local', 'p',
         'p_profile_multiplier', 'ht_bottom', 'den_spec', 't0',
         'direction_spec', 'coordinate_system', 'flow_direction_component',
         'axis_direction_component', 'axis_origin_component', 'ke_spec',
         'nut', 'kl', 'intermit', 'k', 'e', 'o', 'v2', 'turb_intensity',
         'turb_length_scale', 'turb_hydraulic_diam', 'turb_viscosity_ratio',
         'turb_viscosity_ratio_profile', 'rst_spec', 'uu', 'vv', 'ww', 'uv',
         'vw', 'uw', 'ksgs_spec', 'ksgs', 'sgs_turb_intensity',
         'radiation_bc', 'radial_direction_component', 'coll_dtheta',
         'coll_dphi', 'band_q_irrad', 'band_q_irrad_diffuse',
         'parallel_collimated_beam', 'solar_direction', 'solar_irradiation',
         't_b_b_spec', 't_b_b', 'in_emiss', 'fmean', 'fmean2', 'fvar',
         'fvar2', 'granular_temperature', 'iac', 'lsfun', 'vof_spec',
         'volume_fraction', 'species_in_mole_fractions', 'mf',
         'elec_potential_type', 'potential_value', 'dual_potential_type',
         'dual_potential_value', 'x_displacement_type',
         'x_displacement_value', 'y_displacement_type',
         'y_displacement_value', 'z_displacement_type',
         'z_displacement_value', 'prob_mode_1', 'prob_mode_2', 'prob_mode_3',
         'premixc', 'premixc_var', 'ecfm_sigma', 'inert', 'pollut_no',
         'pollut_hcn', 'pollut_nh3', 'pollut_n2o', 'pollut_urea',
         'pollut_hnco', 'pollut_nco', 'pollut_so2', 'pollut_h2s',
         'pollut_so3', 'pollut_sh', 'pollut_so', 'pollut_soot',
         'pollut_nuclei', 'pollut_ctar', 'pollut_hg', 'pollut_hgcl2',
         'pollut_hcl', 'pollut_hgo', 'pollut_cl', 'pollut_cl2', 'pollut_hgcl',
         'pollut_hocl', 'tss_scalar', 'fensapice_flow_bc_subtype', 'uds_bc',
         'uds', 'pb_disc_bc', 'pb_disc', 'pb_qmom_bc', 'pb_qmom', 'pb_smm_bc',
         'pb_smm', 'pb_dqmom_bc', 'pb_dqmom', 'dpm_bc_type',
         'dpm_bc_collision_partner', 'reinj_inj', 'dpm_bc_udf',
         'mixing_plane_thread', 'ac_options', 'p_backflow_spec',
         'p_backflow_spec_gen', 'impedance_0', 'impedance_1', 'impedance_2',
         'ac_wave', 'prevent_reverse_flow', 'radial', 'avg_press_spec',
         'press_averaging_method', 'targeted_mf_boundary', 'targeted_mf',
         'targeted_mf_pmax', 'targeted_mf_pmin', 'gen_nrbc_spec', 'wsf',
         'wsb', 'wsn', 'solar_fluxes', 'solar_shining_factor',
         'radiating_s2s_surface']

    phase: phase = phase
    """
    phase child of pressure_outlet_child
    """
    geom_disable: geom_disable = geom_disable
    """
    geom_disable child of pressure_outlet_child
    """
    geom_dir_spec: geom_dir_spec = geom_dir_spec
    """
    geom_dir_spec child of pressure_outlet_child
    """
    geom_dir_x: geom_dir_x = geom_dir_x
    """
    geom_dir_x child of pressure_outlet_child
    """
    geom_dir_y: geom_dir_y = geom_dir_y
    """
    geom_dir_y child of pressure_outlet_child
    """
    geom_dir_z: geom_dir_z = geom_dir_z
    """
    geom_dir_z child of pressure_outlet_child
    """
    geom_levels: geom_levels = geom_levels
    """
    geom_levels child of pressure_outlet_child
    """
    geom_bgthread: geom_bgthread = geom_bgthread
    """
    geom_bgthread child of pressure_outlet_child
    """
    open_channel: open_channel = open_channel
    """
    open_channel child of pressure_outlet_child
    """
    outlet_number: outlet_number = outlet_number
    """
    outlet_number child of pressure_outlet_child
    """
    pressure_spec_method: pressure_spec_method = pressure_spec_method
    """
    pressure_spec_method child of pressure_outlet_child
    """
    press_spec: press_spec = press_spec
    """
    press_spec child of pressure_outlet_child
    """
    frame_of_reference: frame_of_reference = frame_of_reference
    """
    frame_of_reference child of pressure_outlet_child
    """
    phase_spec: phase_spec = phase_spec
    """
    phase_spec child of pressure_outlet_child
    """
    ht_local: ht_local = ht_local
    """
    ht_local child of pressure_outlet_child
    """
    p: p = p
    """
    p child of pressure_outlet_child
    """
    p_profile_multiplier: p_profile_multiplier = p_profile_multiplier
    """
    p_profile_multiplier child of pressure_outlet_child
    """
    ht_bottom: ht_bottom = ht_bottom
    """
    ht_bottom child of pressure_outlet_child
    """
    den_spec: den_spec = den_spec
    """
    den_spec child of pressure_outlet_child
    """
    t0: t0 = t0
    """
    t0 child of pressure_outlet_child
    """
    direction_spec: direction_spec = direction_spec
    """
    direction_spec child of pressure_outlet_child
    """
    coordinate_system: coordinate_system = coordinate_system
    """
    coordinate_system child of pressure_outlet_child
    """
    flow_direction_component: flow_direction_component = flow_direction_component
    """
    flow_direction_component child of pressure_outlet_child
    """
    axis_direction_component: axis_direction_component = axis_direction_component
    """
    axis_direction_component child of pressure_outlet_child
    """
    axis_origin_component: axis_origin_component = axis_origin_component
    """
    axis_origin_component child of pressure_outlet_child
    """
    ke_spec: ke_spec = ke_spec
    """
    ke_spec child of pressure_outlet_child
    """
    nut: nut = nut
    """
    nut child of pressure_outlet_child
    """
    kl: kl = kl
    """
    kl child of pressure_outlet_child
    """
    intermit: intermit = intermit
    """
    intermit child of pressure_outlet_child
    """
    k: k = k
    """
    k child of pressure_outlet_child
    """
    e: e = e
    """
    e child of pressure_outlet_child
    """
    o: o = o
    """
    o child of pressure_outlet_child
    """
    v2: v2 = v2
    """
    v2 child of pressure_outlet_child
    """
    turb_intensity: turb_intensity = turb_intensity
    """
    turb_intensity child of pressure_outlet_child
    """
    turb_length_scale: turb_length_scale = turb_length_scale
    """
    turb_length_scale child of pressure_outlet_child
    """
    turb_hydraulic_diam: turb_hydraulic_diam = turb_hydraulic_diam
    """
    turb_hydraulic_diam child of pressure_outlet_child
    """
    turb_viscosity_ratio: turb_viscosity_ratio = turb_viscosity_ratio
    """
    turb_viscosity_ratio child of pressure_outlet_child
    """
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile = turb_viscosity_ratio_profile
    """
    turb_viscosity_ratio_profile child of pressure_outlet_child
    """
    rst_spec: rst_spec = rst_spec
    """
    rst_spec child of pressure_outlet_child
    """
    uu: uu = uu
    """
    uu child of pressure_outlet_child
    """
    vv: vv = vv
    """
    vv child of pressure_outlet_child
    """
    ww: ww = ww
    """
    ww child of pressure_outlet_child
    """
    uv: uv = uv
    """
    uv child of pressure_outlet_child
    """
    vw: vw = vw
    """
    vw child of pressure_outlet_child
    """
    uw: uw = uw
    """
    uw child of pressure_outlet_child
    """
    ksgs_spec: ksgs_spec = ksgs_spec
    """
    ksgs_spec child of pressure_outlet_child
    """
    ksgs: ksgs = ksgs
    """
    ksgs child of pressure_outlet_child
    """
    sgs_turb_intensity: sgs_turb_intensity = sgs_turb_intensity
    """
    sgs_turb_intensity child of pressure_outlet_child
    """
    radiation_bc: radiation_bc = radiation_bc
    """
    radiation_bc child of pressure_outlet_child
    """
    radial_direction_component: radial_direction_component = radial_direction_component
    """
    radial_direction_component child of pressure_outlet_child
    """
    coll_dtheta: coll_dtheta = coll_dtheta
    """
    coll_dtheta child of pressure_outlet_child
    """
    coll_dphi: coll_dphi = coll_dphi
    """
    coll_dphi child of pressure_outlet_child
    """
    band_q_irrad: band_q_irrad = band_q_irrad
    """
    band_q_irrad child of pressure_outlet_child
    """
    band_q_irrad_diffuse: band_q_irrad_diffuse = band_q_irrad_diffuse
    """
    band_q_irrad_diffuse child of pressure_outlet_child
    """
    parallel_collimated_beam: parallel_collimated_beam = parallel_collimated_beam
    """
    parallel_collimated_beam child of pressure_outlet_child
    """
    solar_direction: solar_direction = solar_direction
    """
    solar_direction child of pressure_outlet_child
    """
    solar_irradiation: solar_irradiation = solar_irradiation
    """
    solar_irradiation child of pressure_outlet_child
    """
    t_b_b_spec: t_b_b_spec = t_b_b_spec
    """
    t_b_b_spec child of pressure_outlet_child
    """
    t_b_b: t_b_b = t_b_b
    """
    t_b_b child of pressure_outlet_child
    """
    in_emiss: in_emiss = in_emiss
    """
    in_emiss child of pressure_outlet_child
    """
    fmean: fmean = fmean
    """
    fmean child of pressure_outlet_child
    """
    fmean2: fmean2 = fmean2
    """
    fmean2 child of pressure_outlet_child
    """
    fvar: fvar = fvar
    """
    fvar child of pressure_outlet_child
    """
    fvar2: fvar2 = fvar2
    """
    fvar2 child of pressure_outlet_child
    """
    granular_temperature: granular_temperature = granular_temperature
    """
    granular_temperature child of pressure_outlet_child
    """
    iac: iac = iac
    """
    iac child of pressure_outlet_child
    """
    lsfun: lsfun = lsfun
    """
    lsfun child of pressure_outlet_child
    """
    vof_spec: vof_spec = vof_spec
    """
    vof_spec child of pressure_outlet_child
    """
    volume_fraction: volume_fraction = volume_fraction
    """
    volume_fraction child of pressure_outlet_child
    """
    species_in_mole_fractions: species_in_mole_fractions = species_in_mole_fractions
    """
    species_in_mole_fractions child of pressure_outlet_child
    """
    mf: mf = mf
    """
    mf child of pressure_outlet_child
    """
    elec_potential_type: elec_potential_type = elec_potential_type
    """
    elec_potential_type child of pressure_outlet_child
    """
    potential_value: potential_value = potential_value
    """
    potential_value child of pressure_outlet_child
    """
    dual_potential_type: dual_potential_type = dual_potential_type
    """
    dual_potential_type child of pressure_outlet_child
    """
    dual_potential_value: dual_potential_value = dual_potential_value
    """
    dual_potential_value child of pressure_outlet_child
    """
    x_displacement_type: x_displacement_type = x_displacement_type
    """
    x_displacement_type child of pressure_outlet_child
    """
    x_displacement_value: x_displacement_value = x_displacement_value
    """
    x_displacement_value child of pressure_outlet_child
    """
    y_displacement_type: y_displacement_type = y_displacement_type
    """
    y_displacement_type child of pressure_outlet_child
    """
    y_displacement_value: y_displacement_value = y_displacement_value
    """
    y_displacement_value child of pressure_outlet_child
    """
    z_displacement_type: z_displacement_type = z_displacement_type
    """
    z_displacement_type child of pressure_outlet_child
    """
    z_displacement_value: z_displacement_value = z_displacement_value
    """
    z_displacement_value child of pressure_outlet_child
    """
    prob_mode_1: prob_mode_1 = prob_mode_1
    """
    prob_mode_1 child of pressure_outlet_child
    """
    prob_mode_2: prob_mode_2 = prob_mode_2
    """
    prob_mode_2 child of pressure_outlet_child
    """
    prob_mode_3: prob_mode_3 = prob_mode_3
    """
    prob_mode_3 child of pressure_outlet_child
    """
    premixc: premixc = premixc
    """
    premixc child of pressure_outlet_child
    """
    premixc_var: premixc_var = premixc_var
    """
    premixc_var child of pressure_outlet_child
    """
    ecfm_sigma: ecfm_sigma = ecfm_sigma
    """
    ecfm_sigma child of pressure_outlet_child
    """
    inert: inert = inert
    """
    inert child of pressure_outlet_child
    """
    pollut_no: pollut_no = pollut_no
    """
    pollut_no child of pressure_outlet_child
    """
    pollut_hcn: pollut_hcn = pollut_hcn
    """
    pollut_hcn child of pressure_outlet_child
    """
    pollut_nh3: pollut_nh3 = pollut_nh3
    """
    pollut_nh3 child of pressure_outlet_child
    """
    pollut_n2o: pollut_n2o = pollut_n2o
    """
    pollut_n2o child of pressure_outlet_child
    """
    pollut_urea: pollut_urea = pollut_urea
    """
    pollut_urea child of pressure_outlet_child
    """
    pollut_hnco: pollut_hnco = pollut_hnco
    """
    pollut_hnco child of pressure_outlet_child
    """
    pollut_nco: pollut_nco = pollut_nco
    """
    pollut_nco child of pressure_outlet_child
    """
    pollut_so2: pollut_so2 = pollut_so2
    """
    pollut_so2 child of pressure_outlet_child
    """
    pollut_h2s: pollut_h2s = pollut_h2s
    """
    pollut_h2s child of pressure_outlet_child
    """
    pollut_so3: pollut_so3 = pollut_so3
    """
    pollut_so3 child of pressure_outlet_child
    """
    pollut_sh: pollut_sh = pollut_sh
    """
    pollut_sh child of pressure_outlet_child
    """
    pollut_so: pollut_so = pollut_so
    """
    pollut_so child of pressure_outlet_child
    """
    pollut_soot: pollut_soot = pollut_soot
    """
    pollut_soot child of pressure_outlet_child
    """
    pollut_nuclei: pollut_nuclei = pollut_nuclei
    """
    pollut_nuclei child of pressure_outlet_child
    """
    pollut_ctar: pollut_ctar = pollut_ctar
    """
    pollut_ctar child of pressure_outlet_child
    """
    pollut_hg: pollut_hg = pollut_hg
    """
    pollut_hg child of pressure_outlet_child
    """
    pollut_hgcl2: pollut_hgcl2 = pollut_hgcl2
    """
    pollut_hgcl2 child of pressure_outlet_child
    """
    pollut_hcl: pollut_hcl = pollut_hcl
    """
    pollut_hcl child of pressure_outlet_child
    """
    pollut_hgo: pollut_hgo = pollut_hgo
    """
    pollut_hgo child of pressure_outlet_child
    """
    pollut_cl: pollut_cl = pollut_cl
    """
    pollut_cl child of pressure_outlet_child
    """
    pollut_cl2: pollut_cl2 = pollut_cl2
    """
    pollut_cl2 child of pressure_outlet_child
    """
    pollut_hgcl: pollut_hgcl = pollut_hgcl
    """
    pollut_hgcl child of pressure_outlet_child
    """
    pollut_hocl: pollut_hocl = pollut_hocl
    """
    pollut_hocl child of pressure_outlet_child
    """
    tss_scalar: tss_scalar = tss_scalar
    """
    tss_scalar child of pressure_outlet_child
    """
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype = fensapice_flow_bc_subtype
    """
    fensapice_flow_bc_subtype child of pressure_outlet_child
    """
    uds_bc: uds_bc = uds_bc
    """
    uds_bc child of pressure_outlet_child
    """
    uds: uds = uds
    """
    uds child of pressure_outlet_child
    """
    pb_disc_bc: pb_disc_bc = pb_disc_bc
    """
    pb_disc_bc child of pressure_outlet_child
    """
    pb_disc: pb_disc = pb_disc
    """
    pb_disc child of pressure_outlet_child
    """
    pb_qmom_bc: pb_qmom_bc = pb_qmom_bc
    """
    pb_qmom_bc child of pressure_outlet_child
    """
    pb_qmom: pb_qmom = pb_qmom
    """
    pb_qmom child of pressure_outlet_child
    """
    pb_smm_bc: pb_smm_bc = pb_smm_bc
    """
    pb_smm_bc child of pressure_outlet_child
    """
    pb_smm: pb_smm = pb_smm
    """
    pb_smm child of pressure_outlet_child
    """
    pb_dqmom_bc: pb_dqmom_bc = pb_dqmom_bc
    """
    pb_dqmom_bc child of pressure_outlet_child
    """
    pb_dqmom: pb_dqmom = pb_dqmom
    """
    pb_dqmom child of pressure_outlet_child
    """
    dpm_bc_type: dpm_bc_type = dpm_bc_type
    """
    dpm_bc_type child of pressure_outlet_child
    """
    dpm_bc_collision_partner: dpm_bc_collision_partner = dpm_bc_collision_partner
    """
    dpm_bc_collision_partner child of pressure_outlet_child
    """
    reinj_inj: reinj_inj = reinj_inj
    """
    reinj_inj child of pressure_outlet_child
    """
    dpm_bc_udf: dpm_bc_udf = dpm_bc_udf
    """
    dpm_bc_udf child of pressure_outlet_child
    """
    mixing_plane_thread: mixing_plane_thread = mixing_plane_thread
    """
    mixing_plane_thread child of pressure_outlet_child
    """
    ac_options: ac_options = ac_options
    """
    ac_options child of pressure_outlet_child
    """
    p_backflow_spec: p_backflow_spec = p_backflow_spec
    """
    p_backflow_spec child of pressure_outlet_child
    """
    p_backflow_spec_gen: p_backflow_spec_gen = p_backflow_spec_gen
    """
    p_backflow_spec_gen child of pressure_outlet_child
    """
    impedance_0: impedance_0 = impedance_0
    """
    impedance_0 child of pressure_outlet_child
    """
    impedance_1: impedance_1 = impedance_1
    """
    impedance_1 child of pressure_outlet_child
    """
    impedance_2: impedance_2 = impedance_2
    """
    impedance_2 child of pressure_outlet_child
    """
    ac_wave: ac_wave = ac_wave
    """
    ac_wave child of pressure_outlet_child
    """
    prevent_reverse_flow: prevent_reverse_flow = prevent_reverse_flow
    """
    prevent_reverse_flow child of pressure_outlet_child
    """
    radial: radial = radial
    """
    radial child of pressure_outlet_child
    """
    avg_press_spec: avg_press_spec = avg_press_spec
    """
    avg_press_spec child of pressure_outlet_child
    """
    press_averaging_method: press_averaging_method = press_averaging_method
    """
    press_averaging_method child of pressure_outlet_child
    """
    targeted_mf_boundary: targeted_mf_boundary = targeted_mf_boundary
    """
    targeted_mf_boundary child of pressure_outlet_child
    """
    targeted_mf: targeted_mf = targeted_mf
    """
    targeted_mf child of pressure_outlet_child
    """
    targeted_mf_pmax: targeted_mf_pmax = targeted_mf_pmax
    """
    targeted_mf_pmax child of pressure_outlet_child
    """
    targeted_mf_pmin: targeted_mf_pmin = targeted_mf_pmin
    """
    targeted_mf_pmin child of pressure_outlet_child
    """
    gen_nrbc_spec: gen_nrbc_spec = gen_nrbc_spec
    """
    gen_nrbc_spec child of pressure_outlet_child
    """
    wsf: wsf = wsf
    """
    wsf child of pressure_outlet_child
    """
    wsb: wsb = wsb
    """
    wsb child of pressure_outlet_child
    """
    wsn: wsn = wsn
    """
    wsn child of pressure_outlet_child
    """
    solar_fluxes: solar_fluxes = solar_fluxes
    """
    solar_fluxes child of pressure_outlet_child
    """
    solar_shining_factor: solar_shining_factor = solar_shining_factor
    """
    solar_shining_factor child of pressure_outlet_child
    """
    radiating_s2s_surface: radiating_s2s_surface = radiating_s2s_surface
    """
    radiating_s2s_surface child of pressure_outlet_child
    """
