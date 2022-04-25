#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .phase_10 import phase


class network_child(Group):
    """'child_object_type' of network."""

    fluent_name = "child-object-type"

    child_names = ["phase"]

    phase: phase = phase
    """
    phase child of network_child
    """
