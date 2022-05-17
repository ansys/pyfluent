#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .phase_23 import phase
from .geom_disable import geom_disable
from .geom_dir_spec import geom_dir_spec
from .geom_dir_x import geom_dir_x
from .geom_dir_y import geom_dir_y
from .geom_dir_z import geom_dir_z
from .geom_levels import geom_levels
from .geom_bgthread import geom_bgthread
from .open_channel_wave_bc import open_channel_wave_bc
from .ocw_vel_segregated import ocw_vel_segregated
from .velocity_spec import velocity_spec
from .frame_of_reference import frame_of_reference
from .vmag import vmag
from .wave_velocity_spec import wave_velocity_spec
from .avg_flow_velocity import avg_flow_velocity
from .ocw_ship_vel_spec import ocw_ship_vel_spec
from .ocw_ship_vmag import ocw_ship_vmag
from .moving_object_direction_components import moving_object_direction_components
from .ocw_sp_vel_spec import ocw_sp_vel_spec
from .ocw_sp_vmag import ocw_sp_vmag
from .secondary_phase_direction_components import secondary_phase_direction_components
from .ocw_pp_vel_spec import ocw_pp_vel_spec
from .ocw_pp_ref_ht import ocw_pp_ref_ht
from .ocw_pp_power_coeff import ocw_pp_power_coeff
from .ocw_pp_vmag import ocw_pp_vmag
from .ocw_pp_vmag_ref import ocw_pp_vmag_ref
from .primary_phase_direction_components import primary_phase_direction_components
from .p_sup import p_sup
from .coordinate_system import coordinate_system
from .velocity_component import velocity_component
from .flow_direction_component import flow_direction_component
from .axis_direction_component_1 import axis_direction_component
from .axis_origin_component_1 import axis_origin_component
from .omega_swirl import omega_swirl
from .phase_spec import phase_spec
from .wave_bc_type import wave_bc_type
from .ht_local import ht_local
from .ht_bottom import ht_bottom
from .wave_dir_spec import wave_dir_spec
from .wave_modeling_type import wave_modeling_type
from .wave_list import wave_list
from .wave_list_shallow import wave_list_shallow
from .wave_spect_method_freq import wave_spect_method_freq
from .wave_spect_factor import wave_spect_factor
from .wave_spect_sig_wave_ht import wave_spect_sig_wave_ht
from .wave_spect_peak_freq import wave_spect_peak_freq
from .wave_spect_min_freq import wave_spect_min_freq
from .wave_spect_max_freq import wave_spect_max_freq
from .wave_spect_freq_components import wave_spect_freq_components
from .wave_spect_method_dir import wave_spect_method_dir
from .wave_spect_s import wave_spect_s
from .wave_spect_mean_angle import wave_spect_mean_angle
from .wave_spect_deviation import wave_spect_deviation
from .wave_spect_dir_components import wave_spect_dir_components
from .t import t
from .non_equil_boundary import non_equil_boundary
from .tve import tve
from .les_spec_name import les_spec_name
from .rfg_number_of_modes import rfg_number_of_modes
from .vm_number_of_vortices import vm_number_of_vortices
from .vm_streamwise_fluct import vm_streamwise_fluct
from .vm_mass_conservation import vm_mass_conservation
from .volumetric_synthetic_turbulence_generator import volumetric_synthetic_turbulence_generator
from .volumetric_synthetic_turbulence_generator_option import volumetric_synthetic_turbulence_generator_option
from .volumetric_synthetic_turbulence_generator_option_thickness import volumetric_synthetic_turbulence_generator_option_thickness
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
from .granular_temperature import granular_temperature
from .iac import iac
from .lsfun import lsfun
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
from .equ_required import equ_required
from .uds_bc import uds_bc
from .uds import uds
from .pb_disc_bc import pb_disc_bc
from .pb_disc_1 import pb_disc
from .pb_qmom_bc import pb_qmom_bc
from .pb_qmom import pb_qmom
from .pb_smm_bc import pb_smm_bc
from .pb_smm import pb_smm
from .pb_dqmom_bc import pb_dqmom_bc
from .pb_dqmom import pb_dqmom
from .p import p
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
from .tss_scalar import tss_scalar
from .dpm_bc_type import dpm_bc_type
from .dpm_bc_collision_partner import dpm_bc_collision_partner
from .reinj_inj import reinj_inj
from .dpm_bc_udf import dpm_bc_udf
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
from .mixing_plane_thread import mixing_plane_thread
from .solar_fluxes import solar_fluxes
from .solar_shining_factor import solar_shining_factor
from .radiating_s2s_surface import radiating_s2s_surface
from .ac_options import ac_options
from .impedance_0 import impedance_0
from .impedance_1 import impedance_1
from .impedance_2 import impedance_2
from .ac_wave import ac_wave
from .les_spec import les_spec
class velocity_inlet_child(Group):
    """
    'child_object_type' of velocity_inlet
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread', 'open_channel_wave_bc',
         'ocw_vel_segregated', 'velocity_spec', 'frame_of_reference', 'vmag',
         'wave_velocity_spec', 'avg_flow_velocity', 'ocw_ship_vel_spec',
         'ocw_ship_vmag', 'moving_object_direction_components',
         'ocw_sp_vel_spec', 'ocw_sp_vmag',
         'secondary_phase_direction_components', 'ocw_pp_vel_spec',
         'ocw_pp_ref_ht', 'ocw_pp_power_coeff', 'ocw_pp_vmag',
         'ocw_pp_vmag_ref', 'primary_phase_direction_components', 'p_sup',
         'coordinate_system', 'velocity_component',
         'flow_direction_component', 'axis_direction_component',
         'axis_origin_component', 'omega_swirl', 'phase_spec', 'wave_bc_type',
         'ht_local', 'ht_bottom', 'wave_dir_spec', 'wave_modeling_type',
         'wave_list', 'wave_list_shallow', 'wave_spect_method_freq',
         'wave_spect_factor', 'wave_spect_sig_wave_ht',
         'wave_spect_peak_freq', 'wave_spect_min_freq', 'wave_spect_max_freq',
         'wave_spect_freq_components', 'wave_spect_method_dir',
         'wave_spect_s', 'wave_spect_mean_angle', 'wave_spect_deviation',
         'wave_spect_dir_components', 't', 'non_equil_boundary', 'tve',
         'les_spec_name', 'rfg_number_of_modes', 'vm_number_of_vortices',
         'vm_streamwise_fluct', 'vm_mass_conservation',
         'volumetric_synthetic_turbulence_generator',
         'volumetric_synthetic_turbulence_generator_option',
         'volumetric_synthetic_turbulence_generator_option_thickness',
         'ke_spec', 'nut', 'kl', 'intermit', 'k', 'e', 'o', 'v2',
         'turb_intensity', 'turb_length_scale', 'turb_hydraulic_diam',
         'turb_viscosity_ratio', 'turb_viscosity_ratio_profile', 'rst_spec',
         'uu', 'vv', 'ww', 'uv', 'vw', 'uw', 'ksgs_spec', 'ksgs',
         'sgs_turb_intensity', 'granular_temperature', 'iac', 'lsfun',
         'volume_fraction', 'species_in_mole_fractions', 'mf',
         'elec_potential_type', 'potential_value', 'dual_potential_type',
         'dual_potential_value', 'x_displacement_type',
         'x_displacement_value', 'y_displacement_type',
         'y_displacement_value', 'z_displacement_type',
         'z_displacement_value', 'prob_mode_1', 'prob_mode_2', 'prob_mode_3',
         'equ_required', 'uds_bc', 'uds', 'pb_disc_bc', 'pb_disc',
         'pb_qmom_bc', 'pb_qmom', 'pb_smm_bc', 'pb_smm', 'pb_dqmom_bc',
         'pb_dqmom', 'p', 'premixc', 'premixc_var', 'ecfm_sigma', 'inert',
         'pollut_no', 'pollut_hcn', 'pollut_nh3', 'pollut_n2o', 'pollut_urea',
         'pollut_hnco', 'pollut_nco', 'pollut_so2', 'pollut_h2s',
         'pollut_so3', 'pollut_sh', 'pollut_so', 'pollut_soot',
         'pollut_nuclei', 'pollut_ctar', 'pollut_hg', 'pollut_hgcl2',
         'pollut_hcl', 'pollut_hgo', 'pollut_cl', 'pollut_cl2', 'pollut_hgcl',
         'pollut_hocl', 'radiation_bc', 'radial_direction_component',
         'coll_dtheta', 'coll_dphi', 'band_q_irrad', 'band_q_irrad_diffuse',
         'parallel_collimated_beam', 'solar_direction', 'solar_irradiation',
         't_b_b_spec', 't_b_b', 'in_emiss', 'fmean', 'fvar', 'fmean2',
         'fvar2', 'tss_scalar', 'dpm_bc_type', 'dpm_bc_collision_partner',
         'reinj_inj', 'dpm_bc_udf', 'fensapice_flow_bc_subtype',
         'fensapice_drop_bccustom', 'fensapice_drop_lwc',
         'fensapice_drop_dtemp', 'fensapice_drop_ddiam', 'fensapice_drop_dv',
         'fensapice_drop_dx', 'fensapice_drop_dy', 'fensapice_drop_dz',
         'fensapice_dpm_surface_injection', 'fensapice_dpm_inj_nstream',
         'fensapice_drop_icc', 'fensapice_drop_ctemp', 'fensapice_drop_cdiam',
         'fensapice_drop_cv', 'fensapice_drop_cx', 'fensapice_drop_cy',
         'fensapice_drop_cz', 'fensapice_drop_vrh', 'fensapice_drop_vrh_1',
         'fensapice_drop_vc', 'mixing_plane_thread', 'solar_fluxes',
         'solar_shining_factor', 'radiating_s2s_surface', 'ac_options',
         'impedance_0', 'impedance_1', 'impedance_2', 'ac_wave', 'les_spec']

    phase: phase = phase
    """
    phase child of velocity_inlet_child
    """
    geom_disable: geom_disable = geom_disable
    """
    geom_disable child of velocity_inlet_child
    """
    geom_dir_spec: geom_dir_spec = geom_dir_spec
    """
    geom_dir_spec child of velocity_inlet_child
    """
    geom_dir_x: geom_dir_x = geom_dir_x
    """
    geom_dir_x child of velocity_inlet_child
    """
    geom_dir_y: geom_dir_y = geom_dir_y
    """
    geom_dir_y child of velocity_inlet_child
    """
    geom_dir_z: geom_dir_z = geom_dir_z
    """
    geom_dir_z child of velocity_inlet_child
    """
    geom_levels: geom_levels = geom_levels
    """
    geom_levels child of velocity_inlet_child
    """
    geom_bgthread: geom_bgthread = geom_bgthread
    """
    geom_bgthread child of velocity_inlet_child
    """
    open_channel_wave_bc: open_channel_wave_bc = open_channel_wave_bc
    """
    open_channel_wave_bc child of velocity_inlet_child
    """
    ocw_vel_segregated: ocw_vel_segregated = ocw_vel_segregated
    """
    ocw_vel_segregated child of velocity_inlet_child
    """
    velocity_spec: velocity_spec = velocity_spec
    """
    velocity_spec child of velocity_inlet_child
    """
    frame_of_reference: frame_of_reference = frame_of_reference
    """
    frame_of_reference child of velocity_inlet_child
    """
    vmag: vmag = vmag
    """
    vmag child of velocity_inlet_child
    """
    wave_velocity_spec: wave_velocity_spec = wave_velocity_spec
    """
    wave_velocity_spec child of velocity_inlet_child
    """
    avg_flow_velocity: avg_flow_velocity = avg_flow_velocity
    """
    avg_flow_velocity child of velocity_inlet_child
    """
    ocw_ship_vel_spec: ocw_ship_vel_spec = ocw_ship_vel_spec
    """
    ocw_ship_vel_spec child of velocity_inlet_child
    """
    ocw_ship_vmag: ocw_ship_vmag = ocw_ship_vmag
    """
    ocw_ship_vmag child of velocity_inlet_child
    """
    moving_object_direction_components: moving_object_direction_components = moving_object_direction_components
    """
    moving_object_direction_components child of velocity_inlet_child
    """
    ocw_sp_vel_spec: ocw_sp_vel_spec = ocw_sp_vel_spec
    """
    ocw_sp_vel_spec child of velocity_inlet_child
    """
    ocw_sp_vmag: ocw_sp_vmag = ocw_sp_vmag
    """
    ocw_sp_vmag child of velocity_inlet_child
    """
    secondary_phase_direction_components: secondary_phase_direction_components = secondary_phase_direction_components
    """
    secondary_phase_direction_components child of velocity_inlet_child
    """
    ocw_pp_vel_spec: ocw_pp_vel_spec = ocw_pp_vel_spec
    """
    ocw_pp_vel_spec child of velocity_inlet_child
    """
    ocw_pp_ref_ht: ocw_pp_ref_ht = ocw_pp_ref_ht
    """
    ocw_pp_ref_ht child of velocity_inlet_child
    """
    ocw_pp_power_coeff: ocw_pp_power_coeff = ocw_pp_power_coeff
    """
    ocw_pp_power_coeff child of velocity_inlet_child
    """
    ocw_pp_vmag: ocw_pp_vmag = ocw_pp_vmag
    """
    ocw_pp_vmag child of velocity_inlet_child
    """
    ocw_pp_vmag_ref: ocw_pp_vmag_ref = ocw_pp_vmag_ref
    """
    ocw_pp_vmag_ref child of velocity_inlet_child
    """
    primary_phase_direction_components: primary_phase_direction_components = primary_phase_direction_components
    """
    primary_phase_direction_components child of velocity_inlet_child
    """
    p_sup: p_sup = p_sup
    """
    p_sup child of velocity_inlet_child
    """
    coordinate_system: coordinate_system = coordinate_system
    """
    coordinate_system child of velocity_inlet_child
    """
    velocity_component: velocity_component = velocity_component
    """
    velocity_component child of velocity_inlet_child
    """
    flow_direction_component: flow_direction_component = flow_direction_component
    """
    flow_direction_component child of velocity_inlet_child
    """
    axis_direction_component: axis_direction_component = axis_direction_component
    """
    axis_direction_component child of velocity_inlet_child
    """
    axis_origin_component: axis_origin_component = axis_origin_component
    """
    axis_origin_component child of velocity_inlet_child
    """
    omega_swirl: omega_swirl = omega_swirl
    """
    omega_swirl child of velocity_inlet_child
    """
    phase_spec: phase_spec = phase_spec
    """
    phase_spec child of velocity_inlet_child
    """
    wave_bc_type: wave_bc_type = wave_bc_type
    """
    wave_bc_type child of velocity_inlet_child
    """
    ht_local: ht_local = ht_local
    """
    ht_local child of velocity_inlet_child
    """
    ht_bottom: ht_bottom = ht_bottom
    """
    ht_bottom child of velocity_inlet_child
    """
    wave_dir_spec: wave_dir_spec = wave_dir_spec
    """
    wave_dir_spec child of velocity_inlet_child
    """
    wave_modeling_type: wave_modeling_type = wave_modeling_type
    """
    wave_modeling_type child of velocity_inlet_child
    """
    wave_list: wave_list = wave_list
    """
    wave_list child of velocity_inlet_child
    """
    wave_list_shallow: wave_list_shallow = wave_list_shallow
    """
    wave_list_shallow child of velocity_inlet_child
    """
    wave_spect_method_freq: wave_spect_method_freq = wave_spect_method_freq
    """
    wave_spect_method_freq child of velocity_inlet_child
    """
    wave_spect_factor: wave_spect_factor = wave_spect_factor
    """
    wave_spect_factor child of velocity_inlet_child
    """
    wave_spect_sig_wave_ht: wave_spect_sig_wave_ht = wave_spect_sig_wave_ht
    """
    wave_spect_sig_wave_ht child of velocity_inlet_child
    """
    wave_spect_peak_freq: wave_spect_peak_freq = wave_spect_peak_freq
    """
    wave_spect_peak_freq child of velocity_inlet_child
    """
    wave_spect_min_freq: wave_spect_min_freq = wave_spect_min_freq
    """
    wave_spect_min_freq child of velocity_inlet_child
    """
    wave_spect_max_freq: wave_spect_max_freq = wave_spect_max_freq
    """
    wave_spect_max_freq child of velocity_inlet_child
    """
    wave_spect_freq_components: wave_spect_freq_components = wave_spect_freq_components
    """
    wave_spect_freq_components child of velocity_inlet_child
    """
    wave_spect_method_dir: wave_spect_method_dir = wave_spect_method_dir
    """
    wave_spect_method_dir child of velocity_inlet_child
    """
    wave_spect_s: wave_spect_s = wave_spect_s
    """
    wave_spect_s child of velocity_inlet_child
    """
    wave_spect_mean_angle: wave_spect_mean_angle = wave_spect_mean_angle
    """
    wave_spect_mean_angle child of velocity_inlet_child
    """
    wave_spect_deviation: wave_spect_deviation = wave_spect_deviation
    """
    wave_spect_deviation child of velocity_inlet_child
    """
    wave_spect_dir_components: wave_spect_dir_components = wave_spect_dir_components
    """
    wave_spect_dir_components child of velocity_inlet_child
    """
    t: t = t
    """
    t child of velocity_inlet_child
    """
    non_equil_boundary: non_equil_boundary = non_equil_boundary
    """
    non_equil_boundary child of velocity_inlet_child
    """
    tve: tve = tve
    """
    tve child of velocity_inlet_child
    """
    les_spec_name: les_spec_name = les_spec_name
    """
    les_spec_name child of velocity_inlet_child
    """
    rfg_number_of_modes: rfg_number_of_modes = rfg_number_of_modes
    """
    rfg_number_of_modes child of velocity_inlet_child
    """
    vm_number_of_vortices: vm_number_of_vortices = vm_number_of_vortices
    """
    vm_number_of_vortices child of velocity_inlet_child
    """
    vm_streamwise_fluct: vm_streamwise_fluct = vm_streamwise_fluct
    """
    vm_streamwise_fluct child of velocity_inlet_child
    """
    vm_mass_conservation: vm_mass_conservation = vm_mass_conservation
    """
    vm_mass_conservation child of velocity_inlet_child
    """
    volumetric_synthetic_turbulence_generator: volumetric_synthetic_turbulence_generator = volumetric_synthetic_turbulence_generator
    """
    volumetric_synthetic_turbulence_generator child of velocity_inlet_child
    """
    volumetric_synthetic_turbulence_generator_option: volumetric_synthetic_turbulence_generator_option = volumetric_synthetic_turbulence_generator_option
    """
    volumetric_synthetic_turbulence_generator_option child of velocity_inlet_child
    """
    volumetric_synthetic_turbulence_generator_option_thickness: volumetric_synthetic_turbulence_generator_option_thickness = volumetric_synthetic_turbulence_generator_option_thickness
    """
    volumetric_synthetic_turbulence_generator_option_thickness child of velocity_inlet_child
    """
    ke_spec: ke_spec = ke_spec
    """
    ke_spec child of velocity_inlet_child
    """
    nut: nut = nut
    """
    nut child of velocity_inlet_child
    """
    kl: kl = kl
    """
    kl child of velocity_inlet_child
    """
    intermit: intermit = intermit
    """
    intermit child of velocity_inlet_child
    """
    k: k = k
    """
    k child of velocity_inlet_child
    """
    e: e = e
    """
    e child of velocity_inlet_child
    """
    o: o = o
    """
    o child of velocity_inlet_child
    """
    v2: v2 = v2
    """
    v2 child of velocity_inlet_child
    """
    turb_intensity: turb_intensity = turb_intensity
    """
    turb_intensity child of velocity_inlet_child
    """
    turb_length_scale: turb_length_scale = turb_length_scale
    """
    turb_length_scale child of velocity_inlet_child
    """
    turb_hydraulic_diam: turb_hydraulic_diam = turb_hydraulic_diam
    """
    turb_hydraulic_diam child of velocity_inlet_child
    """
    turb_viscosity_ratio: turb_viscosity_ratio = turb_viscosity_ratio
    """
    turb_viscosity_ratio child of velocity_inlet_child
    """
    turb_viscosity_ratio_profile: turb_viscosity_ratio_profile = turb_viscosity_ratio_profile
    """
    turb_viscosity_ratio_profile child of velocity_inlet_child
    """
    rst_spec: rst_spec = rst_spec
    """
    rst_spec child of velocity_inlet_child
    """
    uu: uu = uu
    """
    uu child of velocity_inlet_child
    """
    vv: vv = vv
    """
    vv child of velocity_inlet_child
    """
    ww: ww = ww
    """
    ww child of velocity_inlet_child
    """
    uv: uv = uv
    """
    uv child of velocity_inlet_child
    """
    vw: vw = vw
    """
    vw child of velocity_inlet_child
    """
    uw: uw = uw
    """
    uw child of velocity_inlet_child
    """
    ksgs_spec: ksgs_spec = ksgs_spec
    """
    ksgs_spec child of velocity_inlet_child
    """
    ksgs: ksgs = ksgs
    """
    ksgs child of velocity_inlet_child
    """
    sgs_turb_intensity: sgs_turb_intensity = sgs_turb_intensity
    """
    sgs_turb_intensity child of velocity_inlet_child
    """
    granular_temperature: granular_temperature = granular_temperature
    """
    granular_temperature child of velocity_inlet_child
    """
    iac: iac = iac
    """
    iac child of velocity_inlet_child
    """
    lsfun: lsfun = lsfun
    """
    lsfun child of velocity_inlet_child
    """
    volume_fraction: volume_fraction = volume_fraction
    """
    volume_fraction child of velocity_inlet_child
    """
    species_in_mole_fractions: species_in_mole_fractions = species_in_mole_fractions
    """
    species_in_mole_fractions child of velocity_inlet_child
    """
    mf: mf = mf
    """
    mf child of velocity_inlet_child
    """
    elec_potential_type: elec_potential_type = elec_potential_type
    """
    elec_potential_type child of velocity_inlet_child
    """
    potential_value: potential_value = potential_value
    """
    potential_value child of velocity_inlet_child
    """
    dual_potential_type: dual_potential_type = dual_potential_type
    """
    dual_potential_type child of velocity_inlet_child
    """
    dual_potential_value: dual_potential_value = dual_potential_value
    """
    dual_potential_value child of velocity_inlet_child
    """
    x_displacement_type: x_displacement_type = x_displacement_type
    """
    x_displacement_type child of velocity_inlet_child
    """
    x_displacement_value: x_displacement_value = x_displacement_value
    """
    x_displacement_value child of velocity_inlet_child
    """
    y_displacement_type: y_displacement_type = y_displacement_type
    """
    y_displacement_type child of velocity_inlet_child
    """
    y_displacement_value: y_displacement_value = y_displacement_value
    """
    y_displacement_value child of velocity_inlet_child
    """
    z_displacement_type: z_displacement_type = z_displacement_type
    """
    z_displacement_type child of velocity_inlet_child
    """
    z_displacement_value: z_displacement_value = z_displacement_value
    """
    z_displacement_value child of velocity_inlet_child
    """
    prob_mode_1: prob_mode_1 = prob_mode_1
    """
    prob_mode_1 child of velocity_inlet_child
    """
    prob_mode_2: prob_mode_2 = prob_mode_2
    """
    prob_mode_2 child of velocity_inlet_child
    """
    prob_mode_3: prob_mode_3 = prob_mode_3
    """
    prob_mode_3 child of velocity_inlet_child
    """
    equ_required: equ_required = equ_required
    """
    equ_required child of velocity_inlet_child
    """
    uds_bc: uds_bc = uds_bc
    """
    uds_bc child of velocity_inlet_child
    """
    uds: uds = uds
    """
    uds child of velocity_inlet_child
    """
    pb_disc_bc: pb_disc_bc = pb_disc_bc
    """
    pb_disc_bc child of velocity_inlet_child
    """
    pb_disc: pb_disc = pb_disc
    """
    pb_disc child of velocity_inlet_child
    """
    pb_qmom_bc: pb_qmom_bc = pb_qmom_bc
    """
    pb_qmom_bc child of velocity_inlet_child
    """
    pb_qmom: pb_qmom = pb_qmom
    """
    pb_qmom child of velocity_inlet_child
    """
    pb_smm_bc: pb_smm_bc = pb_smm_bc
    """
    pb_smm_bc child of velocity_inlet_child
    """
    pb_smm: pb_smm = pb_smm
    """
    pb_smm child of velocity_inlet_child
    """
    pb_dqmom_bc: pb_dqmom_bc = pb_dqmom_bc
    """
    pb_dqmom_bc child of velocity_inlet_child
    """
    pb_dqmom: pb_dqmom = pb_dqmom
    """
    pb_dqmom child of velocity_inlet_child
    """
    p: p = p
    """
    p child of velocity_inlet_child
    """
    premixc: premixc = premixc
    """
    premixc child of velocity_inlet_child
    """
    premixc_var: premixc_var = premixc_var
    """
    premixc_var child of velocity_inlet_child
    """
    ecfm_sigma: ecfm_sigma = ecfm_sigma
    """
    ecfm_sigma child of velocity_inlet_child
    """
    inert: inert = inert
    """
    inert child of velocity_inlet_child
    """
    pollut_no: pollut_no = pollut_no
    """
    pollut_no child of velocity_inlet_child
    """
    pollut_hcn: pollut_hcn = pollut_hcn
    """
    pollut_hcn child of velocity_inlet_child
    """
    pollut_nh3: pollut_nh3 = pollut_nh3
    """
    pollut_nh3 child of velocity_inlet_child
    """
    pollut_n2o: pollut_n2o = pollut_n2o
    """
    pollut_n2o child of velocity_inlet_child
    """
    pollut_urea: pollut_urea = pollut_urea
    """
    pollut_urea child of velocity_inlet_child
    """
    pollut_hnco: pollut_hnco = pollut_hnco
    """
    pollut_hnco child of velocity_inlet_child
    """
    pollut_nco: pollut_nco = pollut_nco
    """
    pollut_nco child of velocity_inlet_child
    """
    pollut_so2: pollut_so2 = pollut_so2
    """
    pollut_so2 child of velocity_inlet_child
    """
    pollut_h2s: pollut_h2s = pollut_h2s
    """
    pollut_h2s child of velocity_inlet_child
    """
    pollut_so3: pollut_so3 = pollut_so3
    """
    pollut_so3 child of velocity_inlet_child
    """
    pollut_sh: pollut_sh = pollut_sh
    """
    pollut_sh child of velocity_inlet_child
    """
    pollut_so: pollut_so = pollut_so
    """
    pollut_so child of velocity_inlet_child
    """
    pollut_soot: pollut_soot = pollut_soot
    """
    pollut_soot child of velocity_inlet_child
    """
    pollut_nuclei: pollut_nuclei = pollut_nuclei
    """
    pollut_nuclei child of velocity_inlet_child
    """
    pollut_ctar: pollut_ctar = pollut_ctar
    """
    pollut_ctar child of velocity_inlet_child
    """
    pollut_hg: pollut_hg = pollut_hg
    """
    pollut_hg child of velocity_inlet_child
    """
    pollut_hgcl2: pollut_hgcl2 = pollut_hgcl2
    """
    pollut_hgcl2 child of velocity_inlet_child
    """
    pollut_hcl: pollut_hcl = pollut_hcl
    """
    pollut_hcl child of velocity_inlet_child
    """
    pollut_hgo: pollut_hgo = pollut_hgo
    """
    pollut_hgo child of velocity_inlet_child
    """
    pollut_cl: pollut_cl = pollut_cl
    """
    pollut_cl child of velocity_inlet_child
    """
    pollut_cl2: pollut_cl2 = pollut_cl2
    """
    pollut_cl2 child of velocity_inlet_child
    """
    pollut_hgcl: pollut_hgcl = pollut_hgcl
    """
    pollut_hgcl child of velocity_inlet_child
    """
    pollut_hocl: pollut_hocl = pollut_hocl
    """
    pollut_hocl child of velocity_inlet_child
    """
    radiation_bc: radiation_bc = radiation_bc
    """
    radiation_bc child of velocity_inlet_child
    """
    radial_direction_component: radial_direction_component = radial_direction_component
    """
    radial_direction_component child of velocity_inlet_child
    """
    coll_dtheta: coll_dtheta = coll_dtheta
    """
    coll_dtheta child of velocity_inlet_child
    """
    coll_dphi: coll_dphi = coll_dphi
    """
    coll_dphi child of velocity_inlet_child
    """
    band_q_irrad: band_q_irrad = band_q_irrad
    """
    band_q_irrad child of velocity_inlet_child
    """
    band_q_irrad_diffuse: band_q_irrad_diffuse = band_q_irrad_diffuse
    """
    band_q_irrad_diffuse child of velocity_inlet_child
    """
    parallel_collimated_beam: parallel_collimated_beam = parallel_collimated_beam
    """
    parallel_collimated_beam child of velocity_inlet_child
    """
    solar_direction: solar_direction = solar_direction
    """
    solar_direction child of velocity_inlet_child
    """
    solar_irradiation: solar_irradiation = solar_irradiation
    """
    solar_irradiation child of velocity_inlet_child
    """
    t_b_b_spec: t_b_b_spec = t_b_b_spec
    """
    t_b_b_spec child of velocity_inlet_child
    """
    t_b_b: t_b_b = t_b_b
    """
    t_b_b child of velocity_inlet_child
    """
    in_emiss: in_emiss = in_emiss
    """
    in_emiss child of velocity_inlet_child
    """
    fmean: fmean = fmean
    """
    fmean child of velocity_inlet_child
    """
    fvar: fvar = fvar
    """
    fvar child of velocity_inlet_child
    """
    fmean2: fmean2 = fmean2
    """
    fmean2 child of velocity_inlet_child
    """
    fvar2: fvar2 = fvar2
    """
    fvar2 child of velocity_inlet_child
    """
    tss_scalar: tss_scalar = tss_scalar
    """
    tss_scalar child of velocity_inlet_child
    """
    dpm_bc_type: dpm_bc_type = dpm_bc_type
    """
    dpm_bc_type child of velocity_inlet_child
    """
    dpm_bc_collision_partner: dpm_bc_collision_partner = dpm_bc_collision_partner
    """
    dpm_bc_collision_partner child of velocity_inlet_child
    """
    reinj_inj: reinj_inj = reinj_inj
    """
    reinj_inj child of velocity_inlet_child
    """
    dpm_bc_udf: dpm_bc_udf = dpm_bc_udf
    """
    dpm_bc_udf child of velocity_inlet_child
    """
    fensapice_flow_bc_subtype: fensapice_flow_bc_subtype = fensapice_flow_bc_subtype
    """
    fensapice_flow_bc_subtype child of velocity_inlet_child
    """
    fensapice_drop_bccustom: fensapice_drop_bccustom = fensapice_drop_bccustom
    """
    fensapice_drop_bccustom child of velocity_inlet_child
    """
    fensapice_drop_lwc: fensapice_drop_lwc = fensapice_drop_lwc
    """
    fensapice_drop_lwc child of velocity_inlet_child
    """
    fensapice_drop_dtemp: fensapice_drop_dtemp = fensapice_drop_dtemp
    """
    fensapice_drop_dtemp child of velocity_inlet_child
    """
    fensapice_drop_ddiam: fensapice_drop_ddiam = fensapice_drop_ddiam
    """
    fensapice_drop_ddiam child of velocity_inlet_child
    """
    fensapice_drop_dv: fensapice_drop_dv = fensapice_drop_dv
    """
    fensapice_drop_dv child of velocity_inlet_child
    """
    fensapice_drop_dx: fensapice_drop_dx = fensapice_drop_dx
    """
    fensapice_drop_dx child of velocity_inlet_child
    """
    fensapice_drop_dy: fensapice_drop_dy = fensapice_drop_dy
    """
    fensapice_drop_dy child of velocity_inlet_child
    """
    fensapice_drop_dz: fensapice_drop_dz = fensapice_drop_dz
    """
    fensapice_drop_dz child of velocity_inlet_child
    """
    fensapice_dpm_surface_injection: fensapice_dpm_surface_injection = fensapice_dpm_surface_injection
    """
    fensapice_dpm_surface_injection child of velocity_inlet_child
    """
    fensapice_dpm_inj_nstream: fensapice_dpm_inj_nstream = fensapice_dpm_inj_nstream
    """
    fensapice_dpm_inj_nstream child of velocity_inlet_child
    """
    fensapice_drop_icc: fensapice_drop_icc = fensapice_drop_icc
    """
    fensapice_drop_icc child of velocity_inlet_child
    """
    fensapice_drop_ctemp: fensapice_drop_ctemp = fensapice_drop_ctemp
    """
    fensapice_drop_ctemp child of velocity_inlet_child
    """
    fensapice_drop_cdiam: fensapice_drop_cdiam = fensapice_drop_cdiam
    """
    fensapice_drop_cdiam child of velocity_inlet_child
    """
    fensapice_drop_cv: fensapice_drop_cv = fensapice_drop_cv
    """
    fensapice_drop_cv child of velocity_inlet_child
    """
    fensapice_drop_cx: fensapice_drop_cx = fensapice_drop_cx
    """
    fensapice_drop_cx child of velocity_inlet_child
    """
    fensapice_drop_cy: fensapice_drop_cy = fensapice_drop_cy
    """
    fensapice_drop_cy child of velocity_inlet_child
    """
    fensapice_drop_cz: fensapice_drop_cz = fensapice_drop_cz
    """
    fensapice_drop_cz child of velocity_inlet_child
    """
    fensapice_drop_vrh: fensapice_drop_vrh = fensapice_drop_vrh
    """
    fensapice_drop_vrh child of velocity_inlet_child
    """
    fensapice_drop_vrh_1: fensapice_drop_vrh_1 = fensapice_drop_vrh_1
    """
    fensapice_drop_vrh_1 child of velocity_inlet_child
    """
    fensapice_drop_vc: fensapice_drop_vc = fensapice_drop_vc
    """
    fensapice_drop_vc child of velocity_inlet_child
    """
    mixing_plane_thread: mixing_plane_thread = mixing_plane_thread
    """
    mixing_plane_thread child of velocity_inlet_child
    """
    solar_fluxes: solar_fluxes = solar_fluxes
    """
    solar_fluxes child of velocity_inlet_child
    """
    solar_shining_factor: solar_shining_factor = solar_shining_factor
    """
    solar_shining_factor child of velocity_inlet_child
    """
    radiating_s2s_surface: radiating_s2s_surface = radiating_s2s_surface
    """
    radiating_s2s_surface child of velocity_inlet_child
    """
    ac_options: ac_options = ac_options
    """
    ac_options child of velocity_inlet_child
    """
    impedance_0: impedance_0 = impedance_0
    """
    impedance_0 child of velocity_inlet_child
    """
    impedance_1: impedance_1 = impedance_1
    """
    impedance_1 child of velocity_inlet_child
    """
    impedance_2: impedance_2 = impedance_2
    """
    impedance_2 child of velocity_inlet_child
    """
    ac_wave: ac_wave = ac_wave
    """
    ac_wave child of velocity_inlet_child
    """
    les_spec: les_spec = les_spec
    """
    les_spec child of velocity_inlet_child
    """
