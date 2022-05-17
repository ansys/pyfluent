#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .phase_19 import phase
from .geom_disable import geom_disable
from .geom_dir_spec import geom_dir_spec
from .geom_dir_x import geom_dir_x
from .geom_dir_y import geom_dir_y
from .geom_dir_z import geom_dir_z
from .geom_levels import geom_levels
from .geom_bgthread import geom_bgthread
from .porous_jump_turb_wall_treatment import porous_jump_turb_wall_treatment
from .kc import kc
from .hc import hc
from .t_1 import t
from .q_1 import q
from .dpm_bc_type import dpm_bc_type
from .dpm_bc_collision_partner import dpm_bc_collision_partner
from .reinj_inj import reinj_inj
from .dpm_bc_udf import dpm_bc_udf
from .strength import strength
class radiator_child(Group):
    """
    'child_object_type' of radiator
    """

    fluent_name = "child-object-type"

    child_names = \
        ['phase', 'geom_disable', 'geom_dir_spec', 'geom_dir_x', 'geom_dir_y',
         'geom_dir_z', 'geom_levels', 'geom_bgthread',
         'porous_jump_turb_wall_treatment', 'kc', 'hc', 't', 'q',
         'dpm_bc_type', 'dpm_bc_collision_partner', 'reinj_inj', 'dpm_bc_udf',
         'strength']

    phase: phase = phase
    """
    phase child of radiator_child
    """
    geom_disable: geom_disable = geom_disable
    """
    geom_disable child of radiator_child
    """
    geom_dir_spec: geom_dir_spec = geom_dir_spec
    """
    geom_dir_spec child of radiator_child
    """
    geom_dir_x: geom_dir_x = geom_dir_x
    """
    geom_dir_x child of radiator_child
    """
    geom_dir_y: geom_dir_y = geom_dir_y
    """
    geom_dir_y child of radiator_child
    """
    geom_dir_z: geom_dir_z = geom_dir_z
    """
    geom_dir_z child of radiator_child
    """
    geom_levels: geom_levels = geom_levels
    """
    geom_levels child of radiator_child
    """
    geom_bgthread: geom_bgthread = geom_bgthread
    """
    geom_bgthread child of radiator_child
    """
    porous_jump_turb_wall_treatment: porous_jump_turb_wall_treatment = porous_jump_turb_wall_treatment
    """
    porous_jump_turb_wall_treatment child of radiator_child
    """
    kc: kc = kc
    """
    kc child of radiator_child
    """
    hc: hc = hc
    """
    hc child of radiator_child
    """
    t: t = t
    """
    t child of radiator_child
    """
    q: q = q
    """
    q child of radiator_child
    """
    dpm_bc_type: dpm_bc_type = dpm_bc_type
    """
    dpm_bc_type child of radiator_child
    """
    dpm_bc_collision_partner: dpm_bc_collision_partner = dpm_bc_collision_partner
    """
    dpm_bc_collision_partner child of radiator_child
    """
    reinj_inj: reinj_inj = reinj_inj
    """
    reinj_inj child of radiator_child
    """
    dpm_bc_udf: dpm_bc_udf = dpm_bc_udf
    """
    dpm_bc_udf child of radiator_child
    """
    strength: strength = strength
    """
    strength child of radiator_child
    """
