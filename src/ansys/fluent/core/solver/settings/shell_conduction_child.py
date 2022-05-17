#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from .thickness import thickness
from .material import material
from .qdot import qdot
class shell_conduction_child(Group):
    """
    'child_object_type' of shell_conduction
    """

    fluent_name = "child-object-type"

    child_names = \
        ['thickness', 'material', 'qdot']

    thickness: thickness = thickness
    """
    thickness child of shell_conduction_child
    """
    material: material = material
    """
    material child of shell_conduction_child
    """
    qdot: qdot = qdot
    """
    qdot child of shell_conduction_child
    """
