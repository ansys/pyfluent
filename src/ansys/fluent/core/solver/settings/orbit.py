#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .right import right
from .up import up
class orbit(Command):
    """
    Adjust the camera position without modifying the target.
    
    Parameters
    ----------
        right : real
            'right' child.
        up : real
            'up' child.
    
    """

    fluent_name = "orbit"

    argument_names = \
        ['right', 'up']

    right: right = right
    """
    right argument of orbit
    """
    up: up = up
    """
    up argument of orbit
    """
