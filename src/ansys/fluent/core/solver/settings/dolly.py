#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .in_ import in_
from .right import right
from .up import up


class dolly(Command):
    """Adjust the camera position and target.

    Parameters
    ----------
        right : real
            'right' child.
        up : real
            'up' child.
        in_ : real
            'in' child.
    """

    fluent_name = "dolly"

    argument_names = ["right", "up", "in_"]

    right: right = right
    """
    right argument of dolly
    """
    up: up = up
    """
    up argument of dolly
    """
    in_: in_ = in_
    """
    in_ argument of dolly
    """
