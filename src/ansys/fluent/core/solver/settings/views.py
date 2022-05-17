#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .picture_options import picture_options
from .camera import camera
from .display_states import display_states
from .save_picture import save_picture
from .auto_scale_1 import auto_scale
from .reset_to_default_view import reset_to_default_view
from .delete_view import delete_view
from .last_view import last_view
from .next_view import next_view
from .restore_view import restore_view
from .read_views import read_views
from .save_view import save_view
from .write_views import write_views
class views(Group):
    """
    'views' child.
    """

    fluent_name = "views"

    child_names = \
        ['picture_options', 'camera', 'display_states']

    picture_options: picture_options = picture_options
    """
    picture_options child of views
    """
    camera: camera = camera
    """
    camera child of views
    """
    display_states: display_states = display_states
    """
    display_states child of views
    """
    command_names = \
        ['save_picture', 'auto_scale', 'reset_to_default_view', 'delete_view',
         'last_view', 'next_view', 'restore_view', 'read_views', 'save_view',
         'write_views']

    save_picture: save_picture = save_picture
    """
    save_picture command of views
    """
    auto_scale: auto_scale = auto_scale
    """
    auto_scale command of views
    """
    reset_to_default_view: reset_to_default_view = reset_to_default_view
    """
    reset_to_default_view command of views
    """
    delete_view: delete_view = delete_view
    """
    delete_view command of views
    """
    last_view: last_view = last_view
    """
    last_view command of views
    """
    next_view: next_view = next_view
    """
    next_view command of views
    """
    restore_view: restore_view = restore_view
    """
    restore_view command of views
    """
    read_views: read_views = read_views
    """
    read_views command of views
    """
    save_view: save_view = save_view
    """
    save_view command of views
    """
    write_views: write_views = write_views
    """
    write_views command of views
    """
