#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .phase import phase
from .material import material
from .sources import sources
from .source_terms import source_terms
from .fixed import fixed
from .cylindrical_fixed_var import cylindrical_fixed_var
from .fixes import fixes
from .motion_spec import motion_spec
from .relative_to_thread import relative_to_thread
from .omega import omega
from .axis_origin_component import axis_origin_component
from .axis_direction_component import axis_direction_component
from .udf_zmotion_name import udf_zmotion_name
from .mrf_motion import mrf_motion
from .mrf_relative_to_thread import mrf_relative_to_thread
from .mrf_omega import mrf_omega
from .reference_frame_velocity_components import reference_frame_velocity_components
from .reference_frame_axis_origin_components import reference_frame_axis_origin_components
from .reference_frame_axis_direction_components import reference_frame_axis_direction_components
from .mrf_udf_zmotion_name import mrf_udf_zmotion_name
from .mgrid_enable_transient import mgrid_enable_transient
from .mgrid_motion import mgrid_motion
from .mgrid_relative_to_thread import mgrid_relative_to_thread
from .mgrid_omega import mgrid_omega
from .moving_mesh_velocity_components import moving_mesh_velocity_components
from .moving_mesh_axis_origin_components import moving_mesh_axis_origin_components
from .mgrid_udf_zmotion_name import mgrid_udf_zmotion_name
from .solid_motion import solid_motion
from .solid_relative_to_thread import solid_relative_to_thread
from .solid_omega import solid_omega
from .solid_motion_velocity_components import solid_motion_velocity_components
from .solid_motion_axis_origin_components import solid_motion_axis_origin_components
from .solid_motion_axis_direction_components import solid_motion_axis_direction_components
from .solid_udf_zmotion_name import solid_udf_zmotion_name
from .radiating import radiating
from .les_embedded import les_embedded
from .contact_property import contact_property
from .vapor_phase_realgas import vapor_phase_realgas
from .laminar import laminar
from .laminar_mut_zero import laminar_mut_zero
from .les_embedded_spec import les_embedded_spec
from .les_embedded_mom_scheme import les_embedded_mom_scheme
from .les_embedded_c_wale import les_embedded_c_wale
from .les_embedded_c_smag import les_embedded_c_smag
from .glass import glass
from .porous import porous
from .conical import conical
from .dir_spec_cond import dir_spec_cond
from .cursys import cursys
from .cursys_name import cursys_name
from .direction_1_x import direction_1_x
from .direction_1_y import direction_1_y
from .direction_1_z import direction_1_z
from .direction_2_x import direction_2_x
from .direction_2_y import direction_2_y
from .direction_2_z import direction_2_z
from .cone_axis_x import cone_axis_x
from .cone_axis_y import cone_axis_y
from .cone_axis_z import cone_axis_z
from .cone_axis_pt_x import cone_axis_pt_x
from .cone_axis_pt_y import cone_axis_pt_y
from .cone_axis_pt_z import cone_axis_pt_z
from .cone_angle import cone_angle
from .rel_vel_resistance import rel_vel_resistance
from .porous_r_1 import porous_r_1
from .porous_r_2 import porous_r_2
from .porous_r_3 import porous_r_3
from .alt_inertial_form import alt_inertial_form
from .porous_c_1 import porous_c_1
from .porous_c_2 import porous_c_2
from .porous_c_3 import porous_c_3
from .c0 import c0
from .c1 import c1
from .porosity import porosity
from .viscosity_ratio import viscosity_ratio
from .none import none
from .corey import corey
from .stone_1 import stone_1
from .stone_2 import stone_2
from .rel_perm_limit_p1 import rel_perm_limit_p1
from .rel_perm_limit_p2 import rel_perm_limit_p2
from .ref_perm_p1 import ref_perm_p1
from .exp_p1 import exp_p1
from .res_sat_p1 import res_sat_p1
from .ref_perm_p2 import ref_perm_p2
from .exp_p2 import exp_p2
from .res_sat_p2 import res_sat_p2
from .ref_perm_p3 import ref_perm_p3
from .exp_p3 import exp_p3
from .res_sat_p3 import res_sat_p3
from .capillary_pressure import capillary_pressure
from .max_capillary_pressure import max_capillary_pressure
from .van_genuchten_pg import van_genuchten_pg
from .van_genuchten_ng import van_genuchten_ng
from .skjaeveland_nw_pc_coef import skjaeveland_nw_pc_coef
from .skjaeveland_nw_pc_pwr import skjaeveland_nw_pc_pwr
from .skjaeveland_wet_pc_coef import skjaeveland_wet_pc_coef
from .skjaeveland_wet_pc_pwr import skjaeveland_wet_pc_pwr
from .brooks_corey_pe import brooks_corey_pe
from .brooks_corey_ng import brooks_corey_ng
from .leverett_con_ang import leverett_con_ang
from .rp_cbox_p1 import rp_cbox_p1
from .rp_edit_p1 import rp_edit_p1
from .rel_perm_tabular_p1 import rel_perm_tabular_p1
from .rel_perm_table_p1 import rel_perm_table_p1
from .rel_perm_satw_p1 import rel_perm_satw_p1
from .rel_perm_rp_p1 import rel_perm_rp_p1
from .rp_cbox_p2 import rp_cbox_p2
from .rp_edit_p2 import rp_edit_p2
from .rel_perm_tabular_p2 import rel_perm_tabular_p2
from .rel_perm_table_p2 import rel_perm_table_p2
from .rel_perm_satw_p2 import rel_perm_satw_p2
from .rel_perm_rp_p2 import rel_perm_rp_p2
from .wetting_phase import wetting_phase
from .non_wetting_phase import non_wetting_phase
from .equib_thermal import equib_thermal
from .non_equib_thermal import non_equib_thermal
from .solid_material import solid_material
from .area_density import area_density
from .heat_transfer_coeff import heat_transfer_coeff
from .fanzone import fanzone
from .fan_zone_list import fan_zone_list
from .fan_thickness import fan_thickness
from .fan_hub_rad import fan_hub_rad
from .fan_tip_rad import fan_tip_rad
from .fan_x_origin import fan_x_origin
from .fan_y_origin import fan_y_origin
from .fan_z_origin import fan_z_origin
from .fan_rot_dir import fan_rot_dir
from .fan_opert_angvel import fan_opert_angvel
from .fan_inflection_point import fan_inflection_point
from .limit_flow_fan import limit_flow_fan
from .max_flow_rate import max_flow_rate
from .min_flow_rate import min_flow_rate
from .tan_source_term import tan_source_term
from .rad_source_term import rad_source_term
from .axial_source_term import axial_source_term
from .fan_axial_source_method import fan_axial_source_method
from .fan_pre_jump import fan_pre_jump
from .fan_curve_fit import fan_curve_fit
from .fan_poly_order import fan_poly_order
from .fan_ini_flow import fan_ini_flow
from .fan_test_angvel import fan_test_angvel
from .fan_test_temp import fan_test_temp
from .read_fan_curve import read_fan_curve
from .reaction_mechs_1 import reaction_mechs
from .react import react
from .surface_volume_ratio import surface_volume_ratio
from .electrolyte import electrolyte
from .mp_compressive_beta_max import mp_compressive_beta_max
from .mp_boiling_zone import mp_boiling_zone
from .numerical_beach import numerical_beach
from .beach_id import beach_id
from .beach_multi_dir import beach_multi_dir
from .beach_damp_type import beach_damp_type
from .beach_inlet_bndr import beach_inlet_bndr
from .beach_fs_level import beach_fs_level
from .beach_bottom_level import beach_bottom_level
from .beach_dir_ni import beach_dir_ni
from .beach_dir_nj import beach_dir_nj
from .beach_dir_nk import beach_dir_nk
from .beach_damp_len_spec import beach_damp_len_spec
from .beach_wave_len import beach_wave_len
from .beach_len_factor import beach_len_factor
from .beach_start_point import beach_start_point
from .beach_end_point import beach_end_point
from .beach_dir_list import beach_dir_list
from .beach_damp_relative import beach_damp_relative
from .beach_damp_resist_lin import beach_damp_resist_lin
from .beach_damp_resist import beach_damp_resist
from .porous_structure import porous_structure
from .structure_material import structure_material
from .anisotropic_spe_diff import anisotropic_spe_diff
from .spe_diff_xx import spe_diff_xx
from .spe_diff_xy import spe_diff_xy
from .spe_diff_xz import spe_diff_xz
from .spe_diff_yx import spe_diff_yx
from .spe_diff_yy import spe_diff_yy
from .spe_diff_yz import spe_diff_yz
from .spe_diff_zx import spe_diff_zx
from .spe_diff_zy import spe_diff_zy
from .spe_diff_zz import spe_diff_zz
class fluid_child(Group):
    """
    'child_object_type' of fluid
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'material', 'sources', 'source_terms', 'fixed',
         'cylindrical_fixed_var', 'fixes', 'motion_spec',
         'relative_to_thread', 'omega', 'axis_origin_component',
         'axis_direction_component', 'udf_zmotion_name', 'mrf_motion',
         'mrf_relative_to_thread', 'mrf_omega',
         'reference_frame_velocity_components',
         'reference_frame_axis_origin_components',
         'reference_frame_axis_direction_components', 'mrf_udf_zmotion_name',
         'mgrid_enable_transient', 'mgrid_motion', 'mgrid_relative_to_thread',
         'mgrid_omega', 'moving_mesh_velocity_components',
         'moving_mesh_axis_origin_components', 'mgrid_udf_zmotion_name',
         'solid_motion', 'solid_relative_to_thread', 'solid_omega',
         'solid_motion_velocity_components',
         'solid_motion_axis_origin_components',
         'solid_motion_axis_direction_components', 'solid_udf_zmotion_name',
         'radiating', 'les_embedded', 'contact_property',
         'vapor_phase_realgas', 'laminar', 'laminar_mut_zero',
         'les_embedded_spec', 'les_embedded_mom_scheme',
         'les_embedded_c_wale', 'les_embedded_c_smag', 'glass', 'porous',
         'conical', 'dir_spec_cond', 'cursys', 'cursys_name', 'direction_1_x',
         'direction_1_y', 'direction_1_z', 'direction_2_x', 'direction_2_y',
         'direction_2_z', 'cone_axis_x', 'cone_axis_y', 'cone_axis_z',
         'cone_axis_pt_x', 'cone_axis_pt_y', 'cone_axis_pt_z', 'cone_angle',
         'rel_vel_resistance', 'porous_r_1', 'porous_r_2', 'porous_r_3',
         'alt_inertial_form', 'porous_c_1', 'porous_c_2', 'porous_c_3', 'c0',
         'c1', 'porosity', 'viscosity_ratio', 'none', 'corey', 'stone_1',
         'stone_2', 'rel_perm_limit_p1', 'rel_perm_limit_p2', 'ref_perm_p1',
         'exp_p1', 'res_sat_p1', 'ref_perm_p2', 'exp_p2', 'res_sat_p2',
         'ref_perm_p3', 'exp_p3', 'res_sat_p3', 'capillary_pressure',
         'max_capillary_pressure', 'van_genuchten_pg', 'van_genuchten_ng',
         'skjaeveland_nw_pc_coef', 'skjaeveland_nw_pc_pwr',
         'skjaeveland_wet_pc_coef', 'skjaeveland_wet_pc_pwr',
         'brooks_corey_pe', 'brooks_corey_ng', 'leverett_con_ang',
         'rp_cbox_p1', 'rp_edit_p1', 'rel_perm_tabular_p1',
         'rel_perm_table_p1', 'rel_perm_satw_p1', 'rel_perm_rp_p1',
         'rp_cbox_p2', 'rp_edit_p2', 'rel_perm_tabular_p2',
         'rel_perm_table_p2', 'rel_perm_satw_p2', 'rel_perm_rp_p2',
         'wetting_phase', 'non_wetting_phase', 'equib_thermal',
         'non_equib_thermal', 'solid_material', 'area_density',
         'heat_transfer_coeff', 'fanzone', 'fan_zone_list', 'fan_thickness',
         'fan_hub_rad', 'fan_tip_rad', 'fan_x_origin', 'fan_y_origin',
         'fan_z_origin', 'fan_rot_dir', 'fan_opert_angvel',
         'fan_inflection_point', 'limit_flow_fan', 'max_flow_rate',
         'min_flow_rate', 'tan_source_term', 'rad_source_term',
         'axial_source_term', 'fan_axial_source_method', 'fan_pre_jump',
         'fan_curve_fit', 'fan_poly_order', 'fan_ini_flow', 'fan_test_angvel',
         'fan_test_temp', 'read_fan_curve', 'reaction_mechs', 'react',
         'surface_volume_ratio', 'electrolyte', 'mp_compressive_beta_max',
         'mp_boiling_zone', 'numerical_beach', 'beach_id', 'beach_multi_dir',
         'beach_damp_type', 'beach_inlet_bndr', 'beach_fs_level',
         'beach_bottom_level', 'beach_dir_ni', 'beach_dir_nj', 'beach_dir_nk',
         'beach_damp_len_spec', 'beach_wave_len', 'beach_len_factor',
         'beach_start_point', 'beach_end_point', 'beach_dir_list',
         'beach_damp_relative', 'beach_damp_resist_lin', 'beach_damp_resist',
         'porous_structure', 'structure_material', 'anisotropic_spe_diff',
         'spe_diff_xx', 'spe_diff_xy', 'spe_diff_xz', 'spe_diff_yx',
         'spe_diff_yy', 'spe_diff_yz', 'spe_diff_zx', 'spe_diff_zy',
         'spe_diff_zz']

    phase: phase = phase
    """
    phase child of fluid_child
    """
    material: material = material
    """
    material child of fluid_child
    """
    sources: sources = sources
    """
    sources child of fluid_child
    """
    source_terms: source_terms = source_terms
    """
    source_terms child of fluid_child
    """
    fixed: fixed = fixed
    """
    fixed child of fluid_child
    """
    cylindrical_fixed_var: cylindrical_fixed_var = cylindrical_fixed_var
    """
    cylindrical_fixed_var child of fluid_child
    """
    fixes: fixes = fixes
    """
    fixes child of fluid_child
    """
    motion_spec: motion_spec = motion_spec
    """
    motion_spec child of fluid_child
    """
    relative_to_thread: relative_to_thread = relative_to_thread
    """
    relative_to_thread child of fluid_child
    """
    omega: omega = omega
    """
    omega child of fluid_child
    """
    axis_origin_component: axis_origin_component = axis_origin_component
    """
    axis_origin_component child of fluid_child
    """
    axis_direction_component: axis_direction_component = axis_direction_component
    """
    axis_direction_component child of fluid_child
    """
    udf_zmotion_name: udf_zmotion_name = udf_zmotion_name
    """
    udf_zmotion_name child of fluid_child
    """
    mrf_motion: mrf_motion = mrf_motion
    """
    mrf_motion child of fluid_child
    """
    mrf_relative_to_thread: mrf_relative_to_thread = mrf_relative_to_thread
    """
    mrf_relative_to_thread child of fluid_child
    """
    mrf_omega: mrf_omega = mrf_omega
    """
    mrf_omega child of fluid_child
    """
    reference_frame_velocity_components: reference_frame_velocity_components = reference_frame_velocity_components
    """
    reference_frame_velocity_components child of fluid_child
    """
    reference_frame_axis_origin_components: reference_frame_axis_origin_components = reference_frame_axis_origin_components
    """
    reference_frame_axis_origin_components child of fluid_child
    """
    reference_frame_axis_direction_components: reference_frame_axis_direction_components = reference_frame_axis_direction_components
    """
    reference_frame_axis_direction_components child of fluid_child
    """
    mrf_udf_zmotion_name: mrf_udf_zmotion_name = mrf_udf_zmotion_name
    """
    mrf_udf_zmotion_name child of fluid_child
    """
    mgrid_enable_transient: mgrid_enable_transient = mgrid_enable_transient
    """
    mgrid_enable_transient child of fluid_child
    """
    mgrid_motion: mgrid_motion = mgrid_motion
    """
    mgrid_motion child of fluid_child
    """
    mgrid_relative_to_thread: mgrid_relative_to_thread = mgrid_relative_to_thread
    """
    mgrid_relative_to_thread child of fluid_child
    """
    mgrid_omega: mgrid_omega = mgrid_omega
    """
    mgrid_omega child of fluid_child
    """
    moving_mesh_velocity_components: moving_mesh_velocity_components = moving_mesh_velocity_components
    """
    moving_mesh_velocity_components child of fluid_child
    """
    moving_mesh_axis_origin_components: moving_mesh_axis_origin_components = moving_mesh_axis_origin_components
    """
    moving_mesh_axis_origin_components child of fluid_child
    """
    mgrid_udf_zmotion_name: mgrid_udf_zmotion_name = mgrid_udf_zmotion_name
    """
    mgrid_udf_zmotion_name child of fluid_child
    """
    solid_motion: solid_motion = solid_motion
    """
    solid_motion child of fluid_child
    """
    solid_relative_to_thread: solid_relative_to_thread = solid_relative_to_thread
    """
    solid_relative_to_thread child of fluid_child
    """
    solid_omega: solid_omega = solid_omega
    """
    solid_omega child of fluid_child
    """
    solid_motion_velocity_components: solid_motion_velocity_components = solid_motion_velocity_components
    """
    solid_motion_velocity_components child of fluid_child
    """
    solid_motion_axis_origin_components: solid_motion_axis_origin_components = solid_motion_axis_origin_components
    """
    solid_motion_axis_origin_components child of fluid_child
    """
    solid_motion_axis_direction_components: solid_motion_axis_direction_components = solid_motion_axis_direction_components
    """
    solid_motion_axis_direction_components child of fluid_child
    """
    solid_udf_zmotion_name: solid_udf_zmotion_name = solid_udf_zmotion_name
    """
    solid_udf_zmotion_name child of fluid_child
    """
    radiating: radiating = radiating
    """
    radiating child of fluid_child
    """
    les_embedded: les_embedded = les_embedded
    """
    les_embedded child of fluid_child
    """
    contact_property: contact_property = contact_property
    """
    contact_property child of fluid_child
    """
    vapor_phase_realgas: vapor_phase_realgas = vapor_phase_realgas
    """
    vapor_phase_realgas child of fluid_child
    """
    laminar: laminar = laminar
    """
    laminar child of fluid_child
    """
    laminar_mut_zero: laminar_mut_zero = laminar_mut_zero
    """
    laminar_mut_zero child of fluid_child
    """
    les_embedded_spec: les_embedded_spec = les_embedded_spec
    """
    les_embedded_spec child of fluid_child
    """
    les_embedded_mom_scheme: les_embedded_mom_scheme = les_embedded_mom_scheme
    """
    les_embedded_mom_scheme child of fluid_child
    """
    les_embedded_c_wale: les_embedded_c_wale = les_embedded_c_wale
    """
    les_embedded_c_wale child of fluid_child
    """
    les_embedded_c_smag: les_embedded_c_smag = les_embedded_c_smag
    """
    les_embedded_c_smag child of fluid_child
    """
    glass: glass = glass
    """
    glass child of fluid_child
    """
    porous: porous = porous
    """
    porous child of fluid_child
    """
    conical: conical = conical
    """
    conical child of fluid_child
    """
    dir_spec_cond: dir_spec_cond = dir_spec_cond
    """
    dir_spec_cond child of fluid_child
    """
    cursys: cursys = cursys
    """
    cursys child of fluid_child
    """
    cursys_name: cursys_name = cursys_name
    """
    cursys_name child of fluid_child
    """
    direction_1_x: direction_1_x = direction_1_x
    """
    direction_1_x child of fluid_child
    """
    direction_1_y: direction_1_y = direction_1_y
    """
    direction_1_y child of fluid_child
    """
    direction_1_z: direction_1_z = direction_1_z
    """
    direction_1_z child of fluid_child
    """
    direction_2_x: direction_2_x = direction_2_x
    """
    direction_2_x child of fluid_child
    """
    direction_2_y: direction_2_y = direction_2_y
    """
    direction_2_y child of fluid_child
    """
    direction_2_z: direction_2_z = direction_2_z
    """
    direction_2_z child of fluid_child
    """
    cone_axis_x: cone_axis_x = cone_axis_x
    """
    cone_axis_x child of fluid_child
    """
    cone_axis_y: cone_axis_y = cone_axis_y
    """
    cone_axis_y child of fluid_child
    """
    cone_axis_z: cone_axis_z = cone_axis_z
    """
    cone_axis_z child of fluid_child
    """
    cone_axis_pt_x: cone_axis_pt_x = cone_axis_pt_x
    """
    cone_axis_pt_x child of fluid_child
    """
    cone_axis_pt_y: cone_axis_pt_y = cone_axis_pt_y
    """
    cone_axis_pt_y child of fluid_child
    """
    cone_axis_pt_z: cone_axis_pt_z = cone_axis_pt_z
    """
    cone_axis_pt_z child of fluid_child
    """
    cone_angle: cone_angle = cone_angle
    """
    cone_angle child of fluid_child
    """
    rel_vel_resistance: rel_vel_resistance = rel_vel_resistance
    """
    rel_vel_resistance child of fluid_child
    """
    porous_r_1: porous_r_1 = porous_r_1
    """
    porous_r_1 child of fluid_child
    """
    porous_r_2: porous_r_2 = porous_r_2
    """
    porous_r_2 child of fluid_child
    """
    porous_r_3: porous_r_3 = porous_r_3
    """
    porous_r_3 child of fluid_child
    """
    alt_inertial_form: alt_inertial_form = alt_inertial_form
    """
    alt_inertial_form child of fluid_child
    """
    porous_c_1: porous_c_1 = porous_c_1
    """
    porous_c_1 child of fluid_child
    """
    porous_c_2: porous_c_2 = porous_c_2
    """
    porous_c_2 child of fluid_child
    """
    porous_c_3: porous_c_3 = porous_c_3
    """
    porous_c_3 child of fluid_child
    """
    c0: c0 = c0
    """
    c0 child of fluid_child
    """
    c1: c1 = c1
    """
    c1 child of fluid_child
    """
    porosity: porosity = porosity
    """
    porosity child of fluid_child
    """
    viscosity_ratio: viscosity_ratio = viscosity_ratio
    """
    viscosity_ratio child of fluid_child
    """
    none: none = none
    """
    none child of fluid_child
    """
    corey: corey = corey
    """
    corey child of fluid_child
    """
    stone_1: stone_1 = stone_1
    """
    stone_1 child of fluid_child
    """
    stone_2: stone_2 = stone_2
    """
    stone_2 child of fluid_child
    """
    rel_perm_limit_p1: rel_perm_limit_p1 = rel_perm_limit_p1
    """
    rel_perm_limit_p1 child of fluid_child
    """
    rel_perm_limit_p2: rel_perm_limit_p2 = rel_perm_limit_p2
    """
    rel_perm_limit_p2 child of fluid_child
    """
    ref_perm_p1: ref_perm_p1 = ref_perm_p1
    """
    ref_perm_p1 child of fluid_child
    """
    exp_p1: exp_p1 = exp_p1
    """
    exp_p1 child of fluid_child
    """
    res_sat_p1: res_sat_p1 = res_sat_p1
    """
    res_sat_p1 child of fluid_child
    """
    ref_perm_p2: ref_perm_p2 = ref_perm_p2
    """
    ref_perm_p2 child of fluid_child
    """
    exp_p2: exp_p2 = exp_p2
    """
    exp_p2 child of fluid_child
    """
    res_sat_p2: res_sat_p2 = res_sat_p2
    """
    res_sat_p2 child of fluid_child
    """
    ref_perm_p3: ref_perm_p3 = ref_perm_p3
    """
    ref_perm_p3 child of fluid_child
    """
    exp_p3: exp_p3 = exp_p3
    """
    exp_p3 child of fluid_child
    """
    res_sat_p3: res_sat_p3 = res_sat_p3
    """
    res_sat_p3 child of fluid_child
    """
    capillary_pressure: capillary_pressure = capillary_pressure
    """
    capillary_pressure child of fluid_child
    """
    max_capillary_pressure: max_capillary_pressure = max_capillary_pressure
    """
    max_capillary_pressure child of fluid_child
    """
    van_genuchten_pg: van_genuchten_pg = van_genuchten_pg
    """
    van_genuchten_pg child of fluid_child
    """
    van_genuchten_ng: van_genuchten_ng = van_genuchten_ng
    """
    van_genuchten_ng child of fluid_child
    """
    skjaeveland_nw_pc_coef: skjaeveland_nw_pc_coef = skjaeveland_nw_pc_coef
    """
    skjaeveland_nw_pc_coef child of fluid_child
    """
    skjaeveland_nw_pc_pwr: skjaeveland_nw_pc_pwr = skjaeveland_nw_pc_pwr
    """
    skjaeveland_nw_pc_pwr child of fluid_child
    """
    skjaeveland_wet_pc_coef: skjaeveland_wet_pc_coef = skjaeveland_wet_pc_coef
    """
    skjaeveland_wet_pc_coef child of fluid_child
    """
    skjaeveland_wet_pc_pwr: skjaeveland_wet_pc_pwr = skjaeveland_wet_pc_pwr
    """
    skjaeveland_wet_pc_pwr child of fluid_child
    """
    brooks_corey_pe: brooks_corey_pe = brooks_corey_pe
    """
    brooks_corey_pe child of fluid_child
    """
    brooks_corey_ng: brooks_corey_ng = brooks_corey_ng
    """
    brooks_corey_ng child of fluid_child
    """
    leverett_con_ang: leverett_con_ang = leverett_con_ang
    """
    leverett_con_ang child of fluid_child
    """
    rp_cbox_p1: rp_cbox_p1 = rp_cbox_p1
    """
    rp_cbox_p1 child of fluid_child
    """
    rp_edit_p1: rp_edit_p1 = rp_edit_p1
    """
    rp_edit_p1 child of fluid_child
    """
    rel_perm_tabular_p1: rel_perm_tabular_p1 = rel_perm_tabular_p1
    """
    rel_perm_tabular_p1 child of fluid_child
    """
    rel_perm_table_p1: rel_perm_table_p1 = rel_perm_table_p1
    """
    rel_perm_table_p1 child of fluid_child
    """
    rel_perm_satw_p1: rel_perm_satw_p1 = rel_perm_satw_p1
    """
    rel_perm_satw_p1 child of fluid_child
    """
    rel_perm_rp_p1: rel_perm_rp_p1 = rel_perm_rp_p1
    """
    rel_perm_rp_p1 child of fluid_child
    """
    rp_cbox_p2: rp_cbox_p2 = rp_cbox_p2
    """
    rp_cbox_p2 child of fluid_child
    """
    rp_edit_p2: rp_edit_p2 = rp_edit_p2
    """
    rp_edit_p2 child of fluid_child
    """
    rel_perm_tabular_p2: rel_perm_tabular_p2 = rel_perm_tabular_p2
    """
    rel_perm_tabular_p2 child of fluid_child
    """
    rel_perm_table_p2: rel_perm_table_p2 = rel_perm_table_p2
    """
    rel_perm_table_p2 child of fluid_child
    """
    rel_perm_satw_p2: rel_perm_satw_p2 = rel_perm_satw_p2
    """
    rel_perm_satw_p2 child of fluid_child
    """
    rel_perm_rp_p2: rel_perm_rp_p2 = rel_perm_rp_p2
    """
    rel_perm_rp_p2 child of fluid_child
    """
    wetting_phase: wetting_phase = wetting_phase
    """
    wetting_phase child of fluid_child
    """
    non_wetting_phase: non_wetting_phase = non_wetting_phase
    """
    non_wetting_phase child of fluid_child
    """
    equib_thermal: equib_thermal = equib_thermal
    """
    equib_thermal child of fluid_child
    """
    non_equib_thermal: non_equib_thermal = non_equib_thermal
    """
    non_equib_thermal child of fluid_child
    """
    solid_material: solid_material = solid_material
    """
    solid_material child of fluid_child
    """
    area_density: area_density = area_density
    """
    area_density child of fluid_child
    """
    heat_transfer_coeff: heat_transfer_coeff = heat_transfer_coeff
    """
    heat_transfer_coeff child of fluid_child
    """
    fanzone: fanzone = fanzone
    """
    fanzone child of fluid_child
    """
    fan_zone_list: fan_zone_list = fan_zone_list
    """
    fan_zone_list child of fluid_child
    """
    fan_thickness: fan_thickness = fan_thickness
    """
    fan_thickness child of fluid_child
    """
    fan_hub_rad: fan_hub_rad = fan_hub_rad
    """
    fan_hub_rad child of fluid_child
    """
    fan_tip_rad: fan_tip_rad = fan_tip_rad
    """
    fan_tip_rad child of fluid_child
    """
    fan_x_origin: fan_x_origin = fan_x_origin
    """
    fan_x_origin child of fluid_child
    """
    fan_y_origin: fan_y_origin = fan_y_origin
    """
    fan_y_origin child of fluid_child
    """
    fan_z_origin: fan_z_origin = fan_z_origin
    """
    fan_z_origin child of fluid_child
    """
    fan_rot_dir: fan_rot_dir = fan_rot_dir
    """
    fan_rot_dir child of fluid_child
    """
    fan_opert_angvel: fan_opert_angvel = fan_opert_angvel
    """
    fan_opert_angvel child of fluid_child
    """
    fan_inflection_point: fan_inflection_point = fan_inflection_point
    """
    fan_inflection_point child of fluid_child
    """
    limit_flow_fan: limit_flow_fan = limit_flow_fan
    """
    limit_flow_fan child of fluid_child
    """
    max_flow_rate: max_flow_rate = max_flow_rate
    """
    max_flow_rate child of fluid_child
    """
    min_flow_rate: min_flow_rate = min_flow_rate
    """
    min_flow_rate child of fluid_child
    """
    tan_source_term: tan_source_term = tan_source_term
    """
    tan_source_term child of fluid_child
    """
    rad_source_term: rad_source_term = rad_source_term
    """
    rad_source_term child of fluid_child
    """
    axial_source_term: axial_source_term = axial_source_term
    """
    axial_source_term child of fluid_child
    """
    fan_axial_source_method: fan_axial_source_method = fan_axial_source_method
    """
    fan_axial_source_method child of fluid_child
    """
    fan_pre_jump: fan_pre_jump = fan_pre_jump
    """
    fan_pre_jump child of fluid_child
    """
    fan_curve_fit: fan_curve_fit = fan_curve_fit
    """
    fan_curve_fit child of fluid_child
    """
    fan_poly_order: fan_poly_order = fan_poly_order
    """
    fan_poly_order child of fluid_child
    """
    fan_ini_flow: fan_ini_flow = fan_ini_flow
    """
    fan_ini_flow child of fluid_child
    """
    fan_test_angvel: fan_test_angvel = fan_test_angvel
    """
    fan_test_angvel child of fluid_child
    """
    fan_test_temp: fan_test_temp = fan_test_temp
    """
    fan_test_temp child of fluid_child
    """
    read_fan_curve: read_fan_curve = read_fan_curve
    """
    read_fan_curve child of fluid_child
    """
    reaction_mechs: reaction_mechs = reaction_mechs
    """
    reaction_mechs child of fluid_child
    """
    react: react = react
    """
    react child of fluid_child
    """
    surface_volume_ratio: surface_volume_ratio = surface_volume_ratio
    """
    surface_volume_ratio child of fluid_child
    """
    electrolyte: electrolyte = electrolyte
    """
    electrolyte child of fluid_child
    """
    mp_compressive_beta_max: mp_compressive_beta_max = mp_compressive_beta_max
    """
    mp_compressive_beta_max child of fluid_child
    """
    mp_boiling_zone: mp_boiling_zone = mp_boiling_zone
    """
    mp_boiling_zone child of fluid_child
    """
    numerical_beach: numerical_beach = numerical_beach
    """
    numerical_beach child of fluid_child
    """
    beach_id: beach_id = beach_id
    """
    beach_id child of fluid_child
    """
    beach_multi_dir: beach_multi_dir = beach_multi_dir
    """
    beach_multi_dir child of fluid_child
    """
    beach_damp_type: beach_damp_type = beach_damp_type
    """
    beach_damp_type child of fluid_child
    """
    beach_inlet_bndr: beach_inlet_bndr = beach_inlet_bndr
    """
    beach_inlet_bndr child of fluid_child
    """
    beach_fs_level: beach_fs_level = beach_fs_level
    """
    beach_fs_level child of fluid_child
    """
    beach_bottom_level: beach_bottom_level = beach_bottom_level
    """
    beach_bottom_level child of fluid_child
    """
    beach_dir_ni: beach_dir_ni = beach_dir_ni
    """
    beach_dir_ni child of fluid_child
    """
    beach_dir_nj: beach_dir_nj = beach_dir_nj
    """
    beach_dir_nj child of fluid_child
    """
    beach_dir_nk: beach_dir_nk = beach_dir_nk
    """
    beach_dir_nk child of fluid_child
    """
    beach_damp_len_spec: beach_damp_len_spec = beach_damp_len_spec
    """
    beach_damp_len_spec child of fluid_child
    """
    beach_wave_len: beach_wave_len = beach_wave_len
    """
    beach_wave_len child of fluid_child
    """
    beach_len_factor: beach_len_factor = beach_len_factor
    """
    beach_len_factor child of fluid_child
    """
    beach_start_point: beach_start_point = beach_start_point
    """
    beach_start_point child of fluid_child
    """
    beach_end_point: beach_end_point = beach_end_point
    """
    beach_end_point child of fluid_child
    """
    beach_dir_list: beach_dir_list = beach_dir_list
    """
    beach_dir_list child of fluid_child
    """
    beach_damp_relative: beach_damp_relative = beach_damp_relative
    """
    beach_damp_relative child of fluid_child
    """
    beach_damp_resist_lin: beach_damp_resist_lin = beach_damp_resist_lin
    """
    beach_damp_resist_lin child of fluid_child
    """
    beach_damp_resist: beach_damp_resist = beach_damp_resist
    """
    beach_damp_resist child of fluid_child
    """
    porous_structure: porous_structure = porous_structure
    """
    porous_structure child of fluid_child
    """
    structure_material: structure_material = structure_material
    """
    structure_material child of fluid_child
    """
    anisotropic_spe_diff: anisotropic_spe_diff = anisotropic_spe_diff
    """
    anisotropic_spe_diff child of fluid_child
    """
    spe_diff_xx: spe_diff_xx = spe_diff_xx
    """
    spe_diff_xx child of fluid_child
    """
    spe_diff_xy: spe_diff_xy = spe_diff_xy
    """
    spe_diff_xy child of fluid_child
    """
    spe_diff_xz: spe_diff_xz = spe_diff_xz
    """
    spe_diff_xz child of fluid_child
    """
    spe_diff_yx: spe_diff_yx = spe_diff_yx
    """
    spe_diff_yx child of fluid_child
    """
    spe_diff_yy: spe_diff_yy = spe_diff_yy
    """
    spe_diff_yy child of fluid_child
    """
    spe_diff_yz: spe_diff_yz = spe_diff_yz
    """
    spe_diff_yz child of fluid_child
    """
    spe_diff_zx: spe_diff_zx = spe_diff_zx
    """
    spe_diff_zx child of fluid_child
    """
    spe_diff_zy: spe_diff_zy = spe_diff_zy
    """
    spe_diff_zy child of fluid_child
    """
    spe_diff_zz: spe_diff_zz = spe_diff_zz
    """
    spe_diff_zz child of fluid_child
    """
