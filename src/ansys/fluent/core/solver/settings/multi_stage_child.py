#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .coefficient import coefficient
from .dissipation import dissipation
from .viscous_1 import viscous


class multi_stage_child(Group):
    """'child_object_type' of multi_stage."""

    fluent_name = "child-object-type"

    child_names = ["coefficient", "dissipation", "viscous"]

    coefficient: coefficient = coefficient
    """
    coefficient child of multi_stage_child
    """
    dissipation: dissipation = dissipation
    """
    dissipation child of multi_stage_child
    """
    viscous: viscous = viscous
    """
    viscous child of multi_stage_child
    """
