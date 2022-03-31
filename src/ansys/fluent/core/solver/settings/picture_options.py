#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .color_mode import color_mode
from .dpi import dpi
from .driver_options import driver_options
from .invert_background import invert_background
from .jpeg_hardcopy_quality import jpeg_hardcopy_quality
from .landscape import landscape
from .list_color_mode import list_color_mode
from .preview import preview
from .standard_resolution import standard_resolution
from .use_window_resolution import use_window_resolution
from .x_resolution import x_resolution
from .y_resolution import y_resolution


class picture_options(Group):
    """'picture_options' child."""

    fluent_name = "picture-options"

    child_names = [
        "color_mode",
        "invert_background",
        "driver_options",
        "standard_resolution",
        "jpeg_hardcopy_quality",
        "landscape",
        "x_resolution",
        "y_resolution",
        "dpi",
        "use_window_resolution",
    ]

    color_mode: color_mode = color_mode
    """
    color_mode child of picture_options
    """
    invert_background: invert_background = invert_background
    """
    invert_background child of picture_options
    """
    driver_options: driver_options = driver_options
    """
    driver_options child of picture_options
    """
    standard_resolution: standard_resolution = standard_resolution
    """
    standard_resolution child of picture_options
    """
    jpeg_hardcopy_quality: jpeg_hardcopy_quality = jpeg_hardcopy_quality
    """
    jpeg_hardcopy_quality child of picture_options
    """
    landscape: landscape = landscape
    """
    landscape child of picture_options
    """
    x_resolution: x_resolution = x_resolution
    """
    x_resolution child of picture_options
    """
    y_resolution: y_resolution = y_resolution
    """
    y_resolution child of picture_options
    """
    dpi: dpi = dpi
    """
    dpi child of picture_options
    """
    use_window_resolution: use_window_resolution = use_window_resolution
    """
    use_window_resolution child of picture_options
    """
    command_names = ["list_color_mode", "preview"]

    list_color_mode: list_color_mode = list_color_mode
    """
    list_color_mode command of picture_options
    """
    preview: preview = preview
    """
    preview command of picture_options
    """
