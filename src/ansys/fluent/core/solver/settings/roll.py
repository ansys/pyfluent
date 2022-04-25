#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .counter_clockwise import counter_clockwise


class roll(Command):
    """Adjust the camera up-vector.

    Parameters
    ----------
        counter_clockwise : real
            'counter_clockwise' child.
    """

    fluent_name = "roll"

    argument_names = ["counter_clockwise"]

    counter_clockwise: counter_clockwise = counter_clockwise
    """
    counter_clockwise argument of roll
    """
