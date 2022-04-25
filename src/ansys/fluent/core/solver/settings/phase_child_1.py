#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .axis_direction_component import axis_direction_component
from .axis_origin_component import axis_origin_component
from .contact_property import contact_property
from .cursys import cursys
from .cursys_name import cursys_name
from .cylindrical_fixed_var import cylindrical_fixed_var
from .fixed import fixed
from .fixes import fixes
from .les_embedded import les_embedded
from .material import material
from .mgrid_enable_transient import mgrid_enable_transient
from .mgrid_motion import mgrid_motion
from .mgrid_omega import mgrid_omega
from .mgrid_relative_to_thread import mgrid_relative_to_thread
from .mgrid_udf_zmotion_name import mgrid_udf_zmotion_name
from .motion_spec import motion_spec
from .moving_mesh_axis_origin_components import (
    moving_mesh_axis_origin_components,
)
from .moving_mesh_velocity_components import moving_mesh_velocity_components
from .mrf_motion import mrf_motion
from .mrf_omega import mrf_omega
from .mrf_relative_to_thread import mrf_relative_to_thread
from .mrf_udf_zmotion_name import mrf_udf_zmotion_name
from .omega import omega
from .pcb_model import pcb_model
from .pcb_zone_info import pcb_zone_info
from .radiating import radiating
from .reference_frame_axis_direction_components import (
    reference_frame_axis_direction_components,
)
from .reference_frame_axis_origin_components import (
    reference_frame_axis_origin_components,
)
from .reference_frame_velocity_components import (
    reference_frame_velocity_components,
)
from .relative_to_thread import relative_to_thread
from .solid_motion import solid_motion
from .solid_motion_axis_direction_components import (
    solid_motion_axis_direction_components,
)
from .solid_motion_axis_origin_components import (
    solid_motion_axis_origin_components,
)
from .solid_motion_velocity_components import solid_motion_velocity_components
from .solid_omega import solid_omega
from .solid_relative_to_thread import solid_relative_to_thread
from .solid_udf_zmotion_name import solid_udf_zmotion_name
from .source_terms import source_terms
from .sources import sources
from .udf_zmotion_name import udf_zmotion_name
from .vapor_phase_realgas import vapor_phase_realgas


class phase_child(Group):
    """'child_object_type' of phase."""

    fluent_name = "child-object-type"

    child_names = [
        "material",
        "sources",
        "source_terms",
        "fixed",
        "cylindrical_fixed_var",
        "fixes",
        "motion_spec",
        "relative_to_thread",
        "omega",
        "axis_origin_component",
        "axis_direction_component",
        "udf_zmotion_name",
        "mrf_motion",
        "mrf_relative_to_thread",
        "mrf_omega",
        "reference_frame_velocity_components",
        "reference_frame_axis_origin_components",
        "reference_frame_axis_direction_components",
        "mrf_udf_zmotion_name",
        "mgrid_enable_transient",
        "mgrid_motion",
        "mgrid_relative_to_thread",
        "mgrid_omega",
        "moving_mesh_velocity_components",
        "moving_mesh_axis_origin_components",
        "mgrid_udf_zmotion_name",
        "solid_motion",
        "solid_relative_to_thread",
        "solid_omega",
        "solid_motion_velocity_components",
        "solid_motion_axis_origin_components",
        "solid_motion_axis_direction_components",
        "solid_udf_zmotion_name",
        "radiating",
        "les_embedded",
        "contact_property",
        "vapor_phase_realgas",
        "cursys",
        "cursys_name",
        "pcb_model",
        "pcb_zone_info",
    ]

    material: material = material
    """
    material child of phase_child
    """
    sources: sources = sources
    """
    sources child of phase_child
    """
    source_terms: source_terms = source_terms
    """
    source_terms child of phase_child
    """
    fixed: fixed = fixed
    """
    fixed child of phase_child
    """
    cylindrical_fixed_var: cylindrical_fixed_var = cylindrical_fixed_var
    """
    cylindrical_fixed_var child of phase_child
    """
    fixes: fixes = fixes
    """
    fixes child of phase_child
    """
    motion_spec: motion_spec = motion_spec
    """
    motion_spec child of phase_child
    """
    relative_to_thread: relative_to_thread = relative_to_thread
    """
    relative_to_thread child of phase_child
    """
    omega: omega = omega
    """
    omega child of phase_child
    """
    axis_origin_component: axis_origin_component = axis_origin_component
    """
    axis_origin_component child of phase_child
    """
    axis_direction_component: axis_direction_component = (
        axis_direction_component
    )
    """
    axis_direction_component child of phase_child
    """
    udf_zmotion_name: udf_zmotion_name = udf_zmotion_name
    """
    udf_zmotion_name child of phase_child
    """
    mrf_motion: mrf_motion = mrf_motion
    """
    mrf_motion child of phase_child
    """
    mrf_relative_to_thread: mrf_relative_to_thread = mrf_relative_to_thread
    """
    mrf_relative_to_thread child of phase_child
    """
    mrf_omega: mrf_omega = mrf_omega
    """
    mrf_omega child of phase_child
    """
    reference_frame_velocity_components: reference_frame_velocity_components = (
        reference_frame_velocity_components
    )
    """
    reference_frame_velocity_components child of phase_child
    """
    reference_frame_axis_origin_components: reference_frame_axis_origin_components = (
        reference_frame_axis_origin_components
    )
    """
    reference_frame_axis_origin_components child of phase_child
    """
    reference_frame_axis_direction_components: reference_frame_axis_direction_components = (
        reference_frame_axis_direction_components
    )
    """
    reference_frame_axis_direction_components child of phase_child
    """
    mrf_udf_zmotion_name: mrf_udf_zmotion_name = mrf_udf_zmotion_name
    """
    mrf_udf_zmotion_name child of phase_child
    """
    mgrid_enable_transient: mgrid_enable_transient = mgrid_enable_transient
    """
    mgrid_enable_transient child of phase_child
    """
    mgrid_motion: mgrid_motion = mgrid_motion
    """
    mgrid_motion child of phase_child
    """
    mgrid_relative_to_thread: mgrid_relative_to_thread = (
        mgrid_relative_to_thread
    )
    """
    mgrid_relative_to_thread child of phase_child
    """
    mgrid_omega: mgrid_omega = mgrid_omega
    """
    mgrid_omega child of phase_child
    """
    moving_mesh_velocity_components: moving_mesh_velocity_components = (
        moving_mesh_velocity_components
    )
    """
    moving_mesh_velocity_components child of phase_child
    """
    moving_mesh_axis_origin_components: moving_mesh_axis_origin_components = (
        moving_mesh_axis_origin_components
    )
    """
    moving_mesh_axis_origin_components child of phase_child
    """
    mgrid_udf_zmotion_name: mgrid_udf_zmotion_name = mgrid_udf_zmotion_name
    """
    mgrid_udf_zmotion_name child of phase_child
    """
    solid_motion: solid_motion = solid_motion
    """
    solid_motion child of phase_child
    """
    solid_relative_to_thread: solid_relative_to_thread = (
        solid_relative_to_thread
    )
    """
    solid_relative_to_thread child of phase_child
    """
    solid_omega: solid_omega = solid_omega
    """
    solid_omega child of phase_child
    """
    solid_motion_velocity_components: solid_motion_velocity_components = (
        solid_motion_velocity_components
    )
    """
    solid_motion_velocity_components child of phase_child
    """
    solid_motion_axis_origin_components: solid_motion_axis_origin_components = (
        solid_motion_axis_origin_components
    )
    """
    solid_motion_axis_origin_components child of phase_child
    """
    solid_motion_axis_direction_components: solid_motion_axis_direction_components = (
        solid_motion_axis_direction_components
    )
    """
    solid_motion_axis_direction_components child of phase_child
    """
    solid_udf_zmotion_name: solid_udf_zmotion_name = solid_udf_zmotion_name
    """
    solid_udf_zmotion_name child of phase_child
    """
    radiating: radiating = radiating
    """
    radiating child of phase_child
    """
    les_embedded: les_embedded = les_embedded
    """
    les_embedded child of phase_child
    """
    contact_property: contact_property = contact_property
    """
    contact_property child of phase_child
    """
    vapor_phase_realgas: vapor_phase_realgas = vapor_phase_realgas
    """
    vapor_phase_realgas child of phase_child
    """
    cursys: cursys = cursys
    """
    cursys child of phase_child
    """
    cursys_name: cursys_name = cursys_name
    """
    cursys_name child of phase_child
    """
    pcb_model: pcb_model = pcb_model
    """
    pcb_model child of phase_child
    """
    pcb_zone_info: pcb_zone_info = pcb_zone_info
    """
    pcb_zone_info child of phase_child
    """
