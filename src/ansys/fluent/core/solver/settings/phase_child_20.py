#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .geom_bgthread import geom_bgthread
from .geom_dir_spec import geom_dir_spec
from .geom_dir_x import geom_dir_x
from .geom_dir_y import geom_dir_y
from .geom_dir_z import geom_dir_z
from .geom_disable import geom_disable
from .geom_levels import geom_levels
from .les_embedded_fluctuations import les_embedded_fluctuations
from .les_spec_name import les_spec_name
from .rfg_number_of_modes import rfg_number_of_modes
from .vm_nvortices import vm_nvortices


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
        "les_spec_name",
        "rfg_number_of_modes",
        "vm_nvortices",
        "les_embedded_fluctuations",
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
    les_spec_name: les_spec_name = les_spec_name
    """
    les_spec_name child of phase_child
    """
    rfg_number_of_modes: rfg_number_of_modes = rfg_number_of_modes
    """
    rfg_number_of_modes child of phase_child
    """
    vm_nvortices: vm_nvortices = vm_nvortices
    """
    vm_nvortices child of phase_child
    """
    les_embedded_fluctuations: les_embedded_fluctuations = (
        les_embedded_fluctuations
    )
    """
    les_embedded_fluctuations child of phase_child
    """
