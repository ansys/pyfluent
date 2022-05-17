#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .hardcopy_format import hardcopy_format
from .hardcopy_options import hardcopy_options
from .window_dump_cmd import window_dump_cmd
from .post_format import post_format
from .current_driver import current_driver
class driver_options(Group):
    """
    'driver_options' child.
    """

    fluent_name = "driver-options"

    child_names = \
        ['hardcopy_format', 'hardcopy_options', 'window_dump_cmd',
         'post_format']

    hardcopy_format: hardcopy_format = hardcopy_format
    """
    hardcopy_format child of driver_options
    """
    hardcopy_options: hardcopy_options = hardcopy_options
    """
    hardcopy_options child of driver_options
    """
    window_dump_cmd: window_dump_cmd = window_dump_cmd
    """
    window_dump_cmd child of driver_options
    """
    post_format: post_format = post_format
    """
    post_format child of driver_options
    """
    command_names = \
        ['current_driver']

    current_driver: current_driver = current_driver
    """
    current_driver command of driver_options
    """
