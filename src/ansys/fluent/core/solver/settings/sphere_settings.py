#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .scale_1 import scale
from .sphere_lod import sphere_lod
from .options_8 import options
class sphere_settings(Group):
    """
    'sphere_settings' child.
    """

    fluent_name = "sphere-settings"

    child_names = \
        ['scale', 'sphere_lod', 'options']

    scale: scale = scale
    """
    scale child of sphere_settings
    """
    sphere_lod: sphere_lod = sphere_lod
    """
    sphere_lod child of sphere_settings
    """
    options: options = options
    """
    options child of sphere_settings
    """
