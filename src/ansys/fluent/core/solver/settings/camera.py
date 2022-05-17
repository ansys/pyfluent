#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .dolly import dolly
from .field_1 import field
from .orbit import orbit
from .pan import pan
from .position_1 import position
from .projection import projection
from .roll import roll
from .target import target
from .up_vector import up_vector
from .zoom import zoom
class camera(Group):
    """
    'camera' child.
    """

    fluent_name = "camera"

    command_names = \
        ['dolly', 'field', 'orbit', 'pan', 'position', 'projection', 'roll',
         'target', 'up_vector', 'zoom']

    dolly: dolly = dolly
    """
    dolly command of camera
    """
    field: field = field
    """
    field command of camera
    """
    orbit: orbit = orbit
    """
    orbit command of camera
    """
    pan: pan = pan
    """
    pan command of camera
    """
    position: position = position
    """
    position command of camera
    """
    projection: projection = projection
    """
    projection command of camera
    """
    roll: roll = roll
    """
    roll command of camera
    """
    target: target = target
    """
    target command of camera
    """
    up_vector: up_vector = up_vector
    """
    up_vector command of camera
    """
    zoom: zoom = zoom
    """
    zoom command of camera
    """
