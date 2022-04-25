#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .color_map import color_map
from .display_1 import display
from .display_state_name import display_state_name
from .draw_mesh import draw_mesh
from .field import field
from .gray_scale import gray_scale
from .image_to_display import image_to_display
from .lic_color import lic_color
from .lic_color_by_field import lic_color_by_field
from .lic_fast import lic_fast
from .lic_image_filter import lic_image_filter
from .lic_intensity_alpha import lic_intensity_alpha
from .lic_intensity_factor import lic_intensity_factor
from .lic_max_steps import lic_max_steps
from .lic_normalize import lic_normalize
from .lic_oriented import lic_oriented
from .lic_pixel_interpolation import lic_pixel_interpolation
from .mesh_object import mesh_object
from .name import name
from .range_option import range_option
from .surfaces_list import surfaces_list
from .texture_size import texture_size
from .texture_spacing import texture_spacing
from .vector_field import vector_field


class lic_child(Group):
    """'child_object_type' of lic."""

    fluent_name = "child-object-type"

    child_names = [
        "name",
        "field",
        "vector_field",
        "surfaces_list",
        "lic_color_by_field",
        "lic_color",
        "lic_oriented",
        "lic_normalize",
        "lic_pixel_interpolation",
        "lic_max_steps",
        "texture_spacing",
        "texture_size",
        "lic_intensity_factor",
        "lic_image_filter",
        "lic_intensity_alpha",
        "lic_fast",
        "gray_scale",
        "image_to_display",
        "range_option",
        "color_map",
        "draw_mesh",
        "mesh_object",
        "display_state_name",
    ]

    name: name = name
    """
    name child of lic_child
    """
    field: field = field
    """
    field child of lic_child
    """
    vector_field: vector_field = vector_field
    """
    vector_field child of lic_child
    """
    surfaces_list: surfaces_list = surfaces_list
    """
    surfaces_list child of lic_child
    """
    lic_color_by_field: lic_color_by_field = lic_color_by_field
    """
    lic_color_by_field child of lic_child
    """
    lic_color: lic_color = lic_color
    """
    lic_color child of lic_child
    """
    lic_oriented: lic_oriented = lic_oriented
    """
    lic_oriented child of lic_child
    """
    lic_normalize: lic_normalize = lic_normalize
    """
    lic_normalize child of lic_child
    """
    lic_pixel_interpolation: lic_pixel_interpolation = lic_pixel_interpolation
    """
    lic_pixel_interpolation child of lic_child
    """
    lic_max_steps: lic_max_steps = lic_max_steps
    """
    lic_max_steps child of lic_child
    """
    texture_spacing: texture_spacing = texture_spacing
    """
    texture_spacing child of lic_child
    """
    texture_size: texture_size = texture_size
    """
    texture_size child of lic_child
    """
    lic_intensity_factor: lic_intensity_factor = lic_intensity_factor
    """
    lic_intensity_factor child of lic_child
    """
    lic_image_filter: lic_image_filter = lic_image_filter
    """
    lic_image_filter child of lic_child
    """
    lic_intensity_alpha: lic_intensity_alpha = lic_intensity_alpha
    """
    lic_intensity_alpha child of lic_child
    """
    lic_fast: lic_fast = lic_fast
    """
    lic_fast child of lic_child
    """
    gray_scale: gray_scale = gray_scale
    """
    gray_scale child of lic_child
    """
    image_to_display: image_to_display = image_to_display
    """
    image_to_display child of lic_child
    """
    range_option: range_option = range_option
    """
    range_option child of lic_child
    """
    color_map: color_map = color_map
    """
    color_map child of lic_child
    """
    draw_mesh: draw_mesh = draw_mesh
    """
    draw_mesh child of lic_child
    """
    mesh_object: mesh_object = mesh_object
    """
    mesh_object child of lic_child
    """
    display_state_name: display_state_name = display_state_name
    """
    display_state_name child of lic_child
    """
    command_names = ["display"]

    display: display = display
    """
    display command of lic_child
    """
