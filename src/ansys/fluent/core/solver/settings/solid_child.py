#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .phase_1 import phase
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
from .cursys import cursys
from .cursys_name import cursys_name
from .pcb_model import pcb_model
from .pcb_zone_info import pcb_zone_info
class solid_child(Group):
    """
    'child_object_type' of solid
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
         'vapor_phase_realgas', 'cursys', 'cursys_name', 'pcb_model',
         'pcb_zone_info']

    phase: phase = phase
    """
    phase child of solid_child
    """
    material: material = material
    """
    material child of solid_child
    """
    sources: sources = sources
    """
    sources child of solid_child
    """
    source_terms: source_terms = source_terms
    """
    source_terms child of solid_child
    """
    fixed: fixed = fixed
    """
    fixed child of solid_child
    """
    cylindrical_fixed_var: cylindrical_fixed_var = cylindrical_fixed_var
    """
    cylindrical_fixed_var child of solid_child
    """
    fixes: fixes = fixes
    """
    fixes child of solid_child
    """
    motion_spec: motion_spec = motion_spec
    """
    motion_spec child of solid_child
    """
    relative_to_thread: relative_to_thread = relative_to_thread
    """
    relative_to_thread child of solid_child
    """
    omega: omega = omega
    """
    omega child of solid_child
    """
    axis_origin_component: axis_origin_component = axis_origin_component
    """
    axis_origin_component child of solid_child
    """
    axis_direction_component: axis_direction_component = axis_direction_component
    """
    axis_direction_component child of solid_child
    """
    udf_zmotion_name: udf_zmotion_name = udf_zmotion_name
    """
    udf_zmotion_name child of solid_child
    """
    mrf_motion: mrf_motion = mrf_motion
    """
    mrf_motion child of solid_child
    """
    mrf_relative_to_thread: mrf_relative_to_thread = mrf_relative_to_thread
    """
    mrf_relative_to_thread child of solid_child
    """
    mrf_omega: mrf_omega = mrf_omega
    """
    mrf_omega child of solid_child
    """
    reference_frame_velocity_components: reference_frame_velocity_components = reference_frame_velocity_components
    """
    reference_frame_velocity_components child of solid_child
    """
    reference_frame_axis_origin_components: reference_frame_axis_origin_components = reference_frame_axis_origin_components
    """
    reference_frame_axis_origin_components child of solid_child
    """
    reference_frame_axis_direction_components: reference_frame_axis_direction_components = reference_frame_axis_direction_components
    """
    reference_frame_axis_direction_components child of solid_child
    """
    mrf_udf_zmotion_name: mrf_udf_zmotion_name = mrf_udf_zmotion_name
    """
    mrf_udf_zmotion_name child of solid_child
    """
    mgrid_enable_transient: mgrid_enable_transient = mgrid_enable_transient
    """
    mgrid_enable_transient child of solid_child
    """
    mgrid_motion: mgrid_motion = mgrid_motion
    """
    mgrid_motion child of solid_child
    """
    mgrid_relative_to_thread: mgrid_relative_to_thread = mgrid_relative_to_thread
    """
    mgrid_relative_to_thread child of solid_child
    """
    mgrid_omega: mgrid_omega = mgrid_omega
    """
    mgrid_omega child of solid_child
    """
    moving_mesh_velocity_components: moving_mesh_velocity_components = moving_mesh_velocity_components
    """
    moving_mesh_velocity_components child of solid_child
    """
    moving_mesh_axis_origin_components: moving_mesh_axis_origin_components = moving_mesh_axis_origin_components
    """
    moving_mesh_axis_origin_components child of solid_child
    """
    mgrid_udf_zmotion_name: mgrid_udf_zmotion_name = mgrid_udf_zmotion_name
    """
    mgrid_udf_zmotion_name child of solid_child
    """
    solid_motion: solid_motion = solid_motion
    """
    solid_motion child of solid_child
    """
    solid_relative_to_thread: solid_relative_to_thread = solid_relative_to_thread
    """
    solid_relative_to_thread child of solid_child
    """
    solid_omega: solid_omega = solid_omega
    """
    solid_omega child of solid_child
    """
    solid_motion_velocity_components: solid_motion_velocity_components = solid_motion_velocity_components
    """
    solid_motion_velocity_components child of solid_child
    """
    solid_motion_axis_origin_components: solid_motion_axis_origin_components = solid_motion_axis_origin_components
    """
    solid_motion_axis_origin_components child of solid_child
    """
    solid_motion_axis_direction_components: solid_motion_axis_direction_components = solid_motion_axis_direction_components
    """
    solid_motion_axis_direction_components child of solid_child
    """
    solid_udf_zmotion_name: solid_udf_zmotion_name = solid_udf_zmotion_name
    """
    solid_udf_zmotion_name child of solid_child
    """
    radiating: radiating = radiating
    """
    radiating child of solid_child
    """
    les_embedded: les_embedded = les_embedded
    """
    les_embedded child of solid_child
    """
    contact_property: contact_property = contact_property
    """
    contact_property child of solid_child
    """
    vapor_phase_realgas: vapor_phase_realgas = vapor_phase_realgas
    """
    vapor_phase_realgas child of solid_child
    """
    cursys: cursys = cursys
    """
    cursys child of solid_child
    """
    cursys_name: cursys_name = cursys_name
    """
    cursys_name child of solid_child
    """
    pcb_model: pcb_model = pcb_model
    """
    pcb_model child of solid_child
    """
    pcb_zone_info: pcb_zone_info = pcb_zone_info
    """
    pcb_zone_info child of solid_child
    """
